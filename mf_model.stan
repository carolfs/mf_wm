functions {
    real[] mf(int[,] x, int[] y, real alpha1, real alpha2, real lambda, real beta) {
        real r[250];
        real lftq1[4];
        real rgtq1[4];
        real q2[2];
        for (i in 1:4) {
            lftq1[i] = 0.5;
            rgtq1[i] = 0.5;
        }
        q2[1] = 0.5; // value of blue
        q2[2] = 0.5; // value of pink
        for (t in 1:250) {
            int inist;
            int finst;
            int reward;
            inist = x[t,1];
            finst = x[t,2];
            reward = x[t,3];

            r[t] = beta*(rgtq1[inist] - lftq1[inist]);

            if (y[t] == 0) {
                lftq1[inist] = (1 - alpha1)*lftq1[inist] + alpha1*q2[finst] +
                    alpha1*lambda*(reward - q2[finst]);
            }
            else {
                rgtq1[inist] = (1 - alpha1)*rgtq1[inist] + alpha1*q2[finst] +
                    alpha1*lambda*(reward - q2[finst]);
            }
            q2[finst] = (1 - alpha2)*q2[finst] + alpha2*reward;
        }
        return r;
    }
}
data {
    int<lower=0> N;
    int x[N,250,3];
    int<lower=0, upper=1> y[N,250];
}
transformed data {
}
parameters {
    real<lower=0> alpha1_a;
    real<lower=0> alpha1_b;
    real<lower=0> alpha2_a;
    real<lower=0> alpha2_b;
    real<lower=0> lambda_a;
    real<lower=0> lambda_b;
    real beta_u;
    real<lower=0> beta_s;
    real<lower=0, upper=1> alpha1[N];
    real<lower=0, upper=1> alpha2[N];
    real<lower=0, upper=1> lambda[N];
    real<lower=0> beta[N];
}
transformed parameters {
}
model {
    alpha1_a ~ normal(0, 100);
    alpha1_b ~ normal(0, 100);
    alpha2_a ~ normal(0, 100);
    alpha2_b ~ normal(0, 100);
    lambda_a ~ normal(0, 100);
    lambda_b ~ normal(0, 100);
    beta_u ~ normal(0, 100);
    beta_s ~ normal(0, 100);
    alpha1 ~ beta(alpha1_a, alpha1_b);
    alpha2 ~ beta(alpha2_a, alpha2_b);
    lambda ~ beta(lambda_a, lambda_b);
    beta ~ lognormal(beta_u, beta_s);
    for (i in 1:N)
        y[i] ~ bernoulli_logit(mf(x[i], y[i], alpha1[i], alpha2[i], lambda[i], beta[i]));
}
generated quantities {
}
