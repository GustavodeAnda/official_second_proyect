import pandas as pd
import technical_analysis
import profit_calculator
import technical_indicators
from itertools import combinations
import optuna
from concurrent.futures import ProcessPoolExecutor
import json
import logging

# Configurar el registro
logging.basicConfig(filename='optimization_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def optimize_combination(args):
    combination, data = args
    study = optuna.create_study(direction='maximize')
    study.optimize(func=lambda trial: profit_calculator.profit(trial, data, combination), n_trials=30)
    best_params = study.best_params
    best_value = study.best_value

    logging.info(f"Combination {combination}: Best parameters: {best_params}")
    logging.info(f"Combination {combination}: Best value: {best_value}")

    return combination, best_params, best_value

if __name__ == '__main__':
    # Load data
    data_aapl = pd.read_csv("./data/aapl_project_1m_train.csv").dropna()

    # Calculate technical indicators
    aapl_technical_data = technical_analysis.calculate_technical_indicators(data_aapl)

    # Plot all technical indicators for AAPL
    technical_indicators.plot_technical_indicators(aapl_technical_data, title="AAPL Technical Indicators")

    # Generate all possible combinations of indicators
    indicators = ["RSI", "MACD", "Bollinger Bands", "ATR"]
    all_combinations = []

    for i in range(1, len(indicators) + 1):
        comb = combinations(indicators, i)
        all_combinations.extend(comb)

    # Prepare arguments for multiprocessing
    args = [(combination, data_aapl) for combination in all_combinations]

    # Evaluate all combinations of indicators for AAPL using multiple processes
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(optimize_combination, args))

    best_combination_aapl = None
    best_value_aapl = -float("inf")
    best_params_aapl = None

    for combination, best_params, best_value in results:
        logging.info(f"Final combination {combination}: Best parameters: {best_params}")
        logging.info(f"Final combination {combination}: Best value: {best_value}")

        if best_value > best_value_aapl:
            best_value_aapl = best_value
            best_combination_aapl = combination
            best_params_aapl = best_params

    logging.info(" ")
    logging.info(" ")
    logging.info(
        f"The best combination of indicators for APPLE is: {best_combination_aapl} with a value of: {best_value_aapl}")

    # Crear un diccionario con el mejor resultado
    best_outcome_apple_1min = {
        "combination": best_combination_aapl,
        "value": best_value_aapl,
        "params": best_params_aapl
    }

    logging.info(f"Best outcome: {best_outcome_apple_1min}")

    # Creating a JSON to avoid unnecessary testing
    best_outcome_json = json.dumps(best_outcome_apple_1min, indent=4)

    # Saving file
    with open("best_outcome_apple_1min.txt", "w") as file:
        file.write(best_outcome_json)

