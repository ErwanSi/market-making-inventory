# Tutoriel : Guide Détaillé Pas-à-Pas

Ce document détaille toutes les étapes pour utiliser le projet, de l'installation des prérequis jusqu'à l'analyse des résultats sur des données réelles.

> [!NOTE]
> Ce guide est conçu pour un environnement **Windows**, mais les commandes sont similaires sur Linux/Mac.

---

## 1. Installation de l'Environnement

Avant de pouvoir exécuter le code, il faut préparer un environnement Python isolé.

### Étape 1.1 : Ouvrir le terminal
Ouvrez votre terminal (PowerShell ou Command Prompt) et naviguez jusqu'au dossier du projet :
```powershell
cd c:\Users\Winwin\Desktop\MM\market-making-inventory
```

### Étape 1.2 : Créer un environnement virtuel
Créez un environnement virtuel nommé `venv` pour ne pas mélanger les librairies avec votre système global :
```powershell
python -m venv venv
```

### Étape 1.3 : Activer l'environnement
Activez l'environnement. Vous devriez voir `(venv)` apparaître au début de votre ligne de commande.
```powershell
.\venv\Scripts\activate
```

### Étape 1.4 : Installer les dépendances
Installez toutes les librairies nécessaires listées dans `requirements.txt` :
```powershell
pip install -r requirements.txt
```
*Cela installera notamment : numpy, pandas, matplotlib, stable-baselines3, ccxt (pour les données réelles), etc.*

---

## 2. Premier Test : Simulation Standard

Ce script permet de vérifier que tout fonctionne correctement. Il utilise des données générées mathématiquement (Mouvement Brownien Géométrique) pour comparer deux stratégies.

### Lancer la simulation
Exécutez la commande suivante :
```powershell
python experiments/run_backtest.py
```

### Ce qui se passe :
1. Le script initialise un simulateur de carnet d'ordres.
2. Il exécute la **Stratégie Naïve** (spread fixe, ne gère pas le risque d'inventaire).
3. Il exécute la **Stratégie HJB Optimale** (ajuste les prix pour revenir à un inventaire nul).
4. Il sauvegarde les graphiques de comparaisons dans le dossier `experiments/results/`.

### Analyser les résultats
Allez dans le dossier `experiments/results/` et ouvrez les images :
- `pnl.png` : Compare l'argent gagné cumulé (PnL). La courbe HJB devrait être au-dessus.
- `inventory_dist.png` : Montre la distribution de l'inventaire. HJB devrait être plus centré autour de 0.

---

## 3. Backtest sur Données Réelles (Crypto)

C'est l'étape la plus intéressante. Nous allons tester notre stratégie sur les vrais mouvements de prix du Bitcoin (BTC/USDT) téléchargés depuis Binance.

### Lancer le backtest réel
```powershell
python experiments/run_real_data_backtest.py
```

### Ce qui se passe en détail :
1. **Téléchargement** : Le script se connecte à Binance via la librairie `ccxt` et télécharge les 1000 dernières minutes de prix BTC/USDT.
2. **Estimation** : Il calcule la volatilité réelle du marché sur cette période pour calibrer le modèle.
3. **Simulation** : Il rejoue le marché minute par minute :
   - À chaque pas de temps, l'agent propose des prix d'achat et de vente.
   - Le simulateur vérifie si ces prix auraient été touchés par le vrai prix du marché.
   - Les transactions sont enregistrées et le PnL est mis à jour.
4. **Comparaison** : Il compare encore une fois Naïf vs HJB sur ces données réelles.

### Résultats
Regardez les nouveaux fichiers dans `experiments/results/` :
- `real_price.png` : Le cours du Bitcoin sur la période testée.
- `real_pnl.png` : La performance des stratégies face au marché réel.
- `real_inventory.png` : Comment l'agent a géré ses stocks de bitcoins.

> [!TIP]
> Si la stratégie n'est pas performante, c'est souvent car les paramètres de marché (paramètre A, k) sont calibrés par défaut. Dans un vrai déploiement, il faudrait les estimer dynamiquement.

---

## 4. (Avancé) Entraînement par Renforcement (RL)

Si vous voulez laisser une IA apprendre sa propre stratégie au lieu d'utiliser les mathématiques (HJB).

### Lancer l'entraînement
```powershell
python src/rl_env/train_rl.py
```

### Fonctionnement
- Utilise l'algorithme **PPO** (Proximal Policy Optimization).
- L'agent s'entraîne sur des millions de pas de simulation.
- Le modèle final est sauvegardé dans `models/ppo_market_maker`.

---

## Structure des Dossiers Importants

- `src/models/` : Contient les maths (formules d'Avellaneda).
- `src/data/` : Contient le simulateur et le connecteur Binance.
- `experiments/` : Contient les scripts que vous exécutez (`run_...`).
