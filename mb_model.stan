functions {
    real[] mb(int[,] x, real alpha, real beta) {
        real r[250];
        real v[2];
        v[1] = 0.5; // value of blue
        v[2] = 0.5; // value of pink
        for (t in 1:250) {
            // If right usually goes to pink
            if (x[t,1] == 1)
                r[t] = beta*0.6*(v[2] - v[1]);
            else
                r[t] = beta*0.6*(v[1] - v[2]);
            // If final state is pink
            if (x[t,2] == 1)
                v[2] = (1 - alpha)*v[2] + alpha*x[t,3]; // reward
            else
                v[1] = (1 - alpha)*v[1] + alpha*x[t,3]; // reward
        }
        return r;
    }
}
data {
    int<lower=0> N;
    int<lower=0, upper=1> x[N,250,3];
    int<lower=0, upper=1> y[N,250];
}
transformed data {
}
parameters {
    real<lower=0> alpha_a;
    real<lower=0> alpha_b;
    real beta_u;
    real<lower=0> beta_s;
    real<lower=0, upper=1> alpha[N];
    real<lower=0> beta[N];
}
transformed parameters {
}
model {
    alpha_a ~ normal(0, 100);
    alpha_b ~ normal(0, 100);
    beta_u ~ normal(0, 100);
    beta_s ~ normal(0, 100);
    alpha ~ beta(alpha_a, alpha_b);
    beta ~ lognormal(beta_u, beta_s);
    for (i in 1:N)
        y[i] ~ bernoulli_logit(mb(x[i], alpha[i], beta[i]));
}
generated quantities {
    real alpha_u;
    alpha_u = alpha_a / (alpha_a + alpha_b);
}
