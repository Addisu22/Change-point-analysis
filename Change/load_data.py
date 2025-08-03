# 1. Setup and Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az


#  2. Function: Load and Prepare Data
def load_and_prepare_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True)
        df.set_index('Date', inplace=True)
        df['LogReturn'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
        df.dropna(inplace=True)
        df = df[np.isfinite(df['LogReturn'])]  # Remove infs
        return df
    except Exception as e:
        print("Error loading or preparing data:", str(e))
        return None

def plot_series(df):
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax[0].plot(df.index, df['Price'], color='blue')
    ax[0].set_title("Brent Oil Price Over Time")

    ax[1].plot(df.index, df['LogReturn'], color='orange')
    ax[1].set_title("Log Returns Over Time")

    plt.tight_layout()
    plt.show()

# 3. Function: Visualize Data
def plot_series(df):
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax[0].plot(df.index, df['Price'], color='blue')
    ax[0].set_title("Brent Oil Price Over Time")

    ax[1].plot(df.index, df['LogReturn'], color='orange')
    ax[1].set_title("Log Returns Over Time")

    plt.tight_layout()
    plt.show()

#  4. Function: Bayesian Change Point Detection
def bayesian_change_point_model(log_returns):
    n = len(log_returns)
    with pm.Model() as model:
        # Prior for change point
        tau = pm.DiscreteUniform('tau', lower=0, upper=n)

        # Priors for mean and std before and after tau
        mu_1 = pm.Normal('mu_1', mu=0, sigma=1)
        mu_2 = pm.Normal('mu_2', mu=0, sigma=1)
        sigma = pm.HalfNormal('sigma', sigma=1)

        # Switching mean
        mu = pm.math.switch(tau >= np.arange(n), mu_1, mu_2)

        # Likelihood
        obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=log_returns)

        trace = pm.sample(2000, tune=1000, target_accept=0.95, return_inferencedata=True)

    return model, trace

#  5. Function: Summarize and Plot Results
def summarize_results(trace, df):
    az.plot_trace(trace, var_names=["mu_1", "mu_2", "tau"])
    plt.tight_layout()
    plt.show()

    summary = az.summary(trace, hdi_prob=0.95)
    print(summary)

    # Extract most probable change point
    tau_posterior = trace.posterior['tau'].values.flatten()
    tau_mode = int(np.round(pd.Series(tau_posterior).mode()[0]))
    change_date = df.index[tau_mode]

    mu1 = trace.posterior['mu_1'].mean().item()
    mu2 = trace.posterior['mu_2'].mean().item()
    perc_change = ((mu2 - mu1) / abs(mu1)) * 100

    print(f"\n📌 Change Point Detected Around: {change_date.strftime('%Y-%m-%d')}")
    print(f"Average Return Before Change: {mu1:.5f}")
    print(f"Average Return After Change:  {mu2:.5f}")
    print(f"Change: {perc_change:.2f}%")

    return change_date, mu1, mu2, perc_change
