from logzero import logger as log

import matplotlib.pyplot as plt
import zutils.utils      as zut
import utils_noroot      as utnr
import pandas            as pnd
import os
import tqdm
import zfit
import time

#---------------------------------
class analyzer:
    '''
    This tool is meant to provide diagnostic information on an extended PDF as
    implemented by Zfit
    '''
    #---------------------------------
    def __init__(self, pdf=None):
        self._pdf = pdf
        self._dat = None

        self._d_inival= dict()
        self._d_info  = dict()
        self._out_dir = None
        self._l_nam   = None

        self._initialized = False
    #---------------------------------
    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot make: {value}')
            raise

        self._out_dir = value
    #---------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._check_pdf()
        self._dat = self._pdf.create_sampler(fixed_params=True)
        zfit.settings.set_seed(0)

        self._initialized = True
    #---------------------------------
    def _check_pdf(self):
        if self._pdf is None:
            log.error(f'Missing PDF')
            raise

        if not self._pdf.is_extended:
            log.error(f'Only extended PDFs supported')
            raise

        s_par = self._pdf.get_params()
        self._l_nam = [ par.name for par in s_par ]

        self._d_inival = { par.name : par.value().numpy() for par in s_par }
    #---------------------------------
    def _run_fits(self, mnz, nll, nfit):
        l_res = []
        log.info('Running fits')
        for _ in tqdm.trange(nfit, ascii=' -'):
            self._dat.resample()
            res=mnz.minimize(nll)
            l_res.append(res)

        return l_res
    #---------------------------------
    def _run_hesse(self, l_res):
        log.info('Running Hesse')
        for res in tqdm.tqdm(l_res, ascii=' -'):
            try:
                res.hesse()
            except:
                log.warning('Hesse failed, skipping')
                continue
    #---------------------------------
    def speed(self, nfit=100):
        '''
        Run fit multiple times and time it

        Parameters:
        -------------------
        nfit (int): Number of fits over which to average the fitting time
        '''
        self._initialize()
        log.info(f'Using {nfit} fits')

        nll = zfit.loss.ExtendedUnbinnedNLL(model=self._pdf, data=self._dat)
        mnz = zfit.minimize.Minuit()

        t_1   = time.time()
        l_res = self._run_fits(mnz, nll, nfit)
        t_2   = time.time()
        self._run_hesse(l_res)
        t_3   = time.time()

        t_fit = (t_2 - t_1) / nfit
        t_hes = (t_3 - t_2) / nfit

        self._d_info['Fit/second'] = t_fit
        self._d_info['Hes/second'] = t_hes 
        self._d_info['#Fits']      = nfit 

        log.info(f'Fit takes: {t_fit:.3} seconds')
        log.info(f'Hesse takes: {t_hes:.3} seconds')

        self._finalize()
    #---------------------------------
    def pulls(self, nfit=100):
        '''
        Used to toy fits and make pull distributions 

        Parameters
        ------------------
        nfit (int): Number of fits over which to average the fitting time
        '''
        self._initialize()
        nll     = zfit.loss.ExtendedUnbinnedNLL(model=self._pdf, data=self._dat)
        mnz     = zfit.minimize.Minuit()

        l_res = self._run_fits(mnz, nll, nfit)
        self._run_hesse(l_res)
        self._make_pulls(l_res)
    #---------------------------------
    def _get_val_err(self, res):
        l_val = []
        l_err = []

        res.freeze()
        for nam in self._l_nam:
            d_val = res.params[nam]
            val   = d_val['value']
            err   = d_val['hesse']['error'] 

            l_val.append(val)
            l_err.append(err)

        return l_val, l_err
    #---------------------------------
    def _get_fit_df(self, l_res):
        df_val = pnd.DataFrame(columns=self._l_nam)
        df_err = pnd.DataFrame(columns=self._l_nam)

        for res in l_res:
            l_val, l_err = self._get_val_err(res)

            df_val = utnr.add_row_to_df(df_val, l_val)
            df_err = utnr.add_row_to_df(df_err, l_err)

        return df_val, df_err
    #---------------------------------
    def _make_pulls(self, l_res):
        df_val, df_err = self._get_fit_df(l_res)

        for nam in self._l_nam:
            pull = (df_val[nam] - self._d_inival[nam]) / df_err[nam]
            pull.hist(bins=30, range=[-4, +4])
            pull_path=f'{self._out_dir}/{nam}.png'
            log.info(f'Saving to: {pull_path}')
            plt.savefig(pull_path)
            plt.close('all')
    #---------------------------------
    def _finalize(self):
        out_path = f'{self._out_dir}/info.json'
        utnr.dump_json(self._d_info, out_path)

        log.info(f'Saving to: {out_path}')
#---------------------------------

