data {
    int M; // number of participants
    int N; // number of trials
    int K; // number of predictors
    int<lower=0, upper=1> y[M,N]; // stay
    matrix[N, K] x[M]; // predictors
    int<lower=0, upper=1> group[M]; // group (0: control, 1: exp)
}
parameters {
    // Individual effects
    vector[K] beta[M];
    // Group effects
    vector[K] usim;
    vector[K] useq;
    // Variance
    vector<lower=0>[K] sigma;
}
transformed parameters {
}

model {
    usim ~ normal(0, 5);
    useq ~ normal(0, 5);
    sigma ~ normal(0, 5);
    for (i in 1:M) {
        beta[i] ~ normal((1 - group[i])*usim + group[i]*useq, sigma);
        y[i] ~ bernoulli_logit(x[i] * beta[i]);
    }
}

generated quantities {
    vector[K] diff;
    diff = useq - usim;
}
