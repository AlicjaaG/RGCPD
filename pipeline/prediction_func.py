import func_models as fc_utils
from stat_models_cont import ScikitModel
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.linear_model import LogisticRegressionCV


def pred(rg, prediction = 'events', q = 0.66):
    if prediction == 'continuous':
        model = ScikitModel(Ridge, verbosity=0)
        # You can also tune parameters by passing a list of values. Then GridSearchCV from sklearn will 
        # find the set of parameters that give the best mean score on all kfold test sets. 
        # below we pass a list of alpha's to tune the regularization.
        alphas = list(np.concatenate([[1E-20],np.logspace(-5,0, 6), np.logspace(.01, 2.5, num=25)]))                       
        kwrgs_model = {'scoringCV':'neg_mean_absolute_error',
                       'kfold':5,
                       'alpha':alphas} # large a, strong regul.
    elif prediction == 'events':
        model = ScikitModel(LogisticRegressionCV, verbosity=0)
        kwrgs_model = {'kfold':5,
                       'scoring':'neg_brier_score'}

    target_ts = rg.TV.RV_ts ; 
    target_ts = (target_ts - target_ts.mean()) / target_ts.std()
    if prediction == 'events':
        if q >= 0.5:
            target_ts = (target_ts > target_ts.quantile(q)).astype(int)
        elif q < .5:
            target_ts = (target_ts < target_ts.quantile(q)).astype(int)
        BSS = fc_utils.ErrorSkillScore(constant_bench=float(target_ts.mean())).BSS
        score_func_list = [BSS, fc_utils.metrics.roc_auc_score]

    elif prediction == 'continuous':
        RMSE_SS = fc_utils.ErrorSkillScore(constant_bench=float(target_ts.mean())).RMSE
        MAE_SS = fc_utils.ErrorSkillScore(constant_bench=float(target_ts.mean())).MAE
        score_func_list = [RMSE_SS, fc_utils.corrcoef, MAE_SS]


    keys = [k for k in rg.df_data.columns[1:-2]]
    out = rg.fit_df_data_ridge(target=target_ts,
                                keys=keys, 
                                fcmodel=model,
                                kwrgs_model=kwrgs_model,
                                transformer=None,
                                tau_min=0, tau_max=0) # <- lag should be zero
    predict, weights, model_lags = out

    df_train_m, df_test_s_m, df_test_m, df_boot = fc_utils.get_scores(predict,
                                                                     rg.df_data.iloc[:,-2:],
                                                                     score_func_list,
                                                                     n_boot = 100, # bootstrapping for Conf. Intervals
                                                                     score_per_test=False,
                                                                     blocksize=1,
                                                                     rng_seed=1)
    if prediction == 'events':
        print(model.scikitmodel.__name__, '\n', f'Test score\n',
              'BSS {:.2f}\n'.format(df_test_m.loc[0].loc[0].loc['BSS']),
              'AUC {:.2f}'.format(df_test_m.loc[0].loc[0].loc['roc_auc_score']),
              '\nTrain score\n',
              'BSS {:.2f}\n'.format(df_train_m.mean(0).loc[0]['BSS']),
              'AUC {:.2f}'.format(df_train_m.mean(0).loc[0]['roc_auc_score']))
        auc_train = df_train_m.mean(0).loc[0]['roc_auc_score']
        auc_test = df_test_m.loc[0].loc[0].loc['roc_auc_score']
        bss_test = df_test_m.mean(0).loc[0]['BSS']
        return auc_test, bss_test
    elif prediction == 'continuous':
        print(model.scikitmodel.__name__, '\n', 'Test score\n',
              'RMSE {:.2f}\n'.format(df_test_m.loc[0][0]['RMSE']),
              'MAE {:.2f}\n'.format(df_test_m.loc[0][0]['MAE']),
              'corrcoef {:.2f}'.format(df_test_m.loc[0][0]['corrcoef']),
              '\nTrain score\n',
              'RMSE {:.2f}\n'.format(df_train_m.mean(0).loc[0]['RMSE']),
              'MAE {:.2f}\n'.format(df_train_m.mean(0).loc[0]['MAE']),
              'corrcoef {:.2f}'.format(df_train_m.mean(0).loc[0]['corrcoef']))