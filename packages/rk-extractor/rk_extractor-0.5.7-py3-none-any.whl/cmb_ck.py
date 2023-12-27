import os
import math
import numpy
import jacobi            as jac
import matplotlib.pyplot as plt

from logzero import logger as log
#----------------------------------------
class combiner:
    '''
    Class used to combine CK values from multiple datasets into
    a combined one
    '''
    #----------------------------------------
    def __init__(self, rjp=None, eff=None, cov=None):
        '''
        rjp (dict): It holds the values of rjpsi e.g. {'2017_TIS' : 1.02...}
        eff (dict): It holds the muon and electron full efficiencies, e.g. {'r1_TOS' : (eff_mu, eff_ee)}
        cov (narray): It's the NxN covariance matrix associated to CK, running over triggers and datasets
        '''

        self._d_rjpsi = rjp
        self._d_eff   = eff
        self._cov     = cov
        self._l_dset  = ['r1', 'r2p1', '2017', '2018']
        self._l_trig  = ['TOS', 'TIS']

        self._out_dir     = None
        self._initialized = False
    #----------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        right_sizes = len(self._d_rjpsi)   == len(self._d_eff) == self._cov.shape[0] == self._cov.shape[1]
        right_keys  = self._d_rjpsi.keys() == self._d_eff.keys()

        if not right_sizes:
            log.error(f'Sizes of inputs is wrong:')
            raise

        if not right_keys:
            log.error(f'Sizes of input dictionaries are different')
            raise

        self._initialized = True
    #----------------------------------------
    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot make directory: {value}')
            raise
        self._out_dir = value
    #----------------------------------------
    def _get_ck(self):
        l_ck_tos = []
        l_ck_tis = []
        for dset in self._l_dset:
            for trig in self._l_trig:
                key = f'{dset}_{trig}'
                eff_mm, eff_ee = self._d_eff[key]
                rjpsi          = self._d_rjpsi[key]
                ck             = (eff_ee / eff_mm) / rjpsi
                if trig == 'TOS':
                    l_ck_tos.append(ck)
                else:
                    l_ck_tis.append(ck)

        return numpy.array(l_ck_tos), numpy.array(l_ck_tis)
    #----------------------------------------
    def _get_cov(self, trig=None):
        l_ind = [0, 2, 4, 6] if trig == 'TIS' else [1, 3, 5, 7]

        cov = self._cov
        cov = numpy.delete(cov, l_ind, axis=0)
        cov = numpy.delete(cov, l_ind, axis=1)

        return cov
    #----------------------------------------
    def _plot_avg(self, mu=None, sg=None, arr=None, mat=None, preffix=None):
        if self._out_dir is None:
            return

        l_var=numpy.diag(mat)
        l_err=[math.sqrt(var) for var in l_var]

        plt.errorbar(x=self._l_dset, y=arr, yerr=l_err, label='Measured')
        plt.gca().axhline(y=mu     , linestyle='-', color='r', label='Average')
        plt.gca().axhline(y=mu + sg, linestyle=':', color='r', label=r'$+\sigma$')
        plt.gca().axhline(y=mu - sg, linestyle=':', color='r', label=r'$-\sigma$')
        plt.ylabel(r'$\frac{\varepsilon(ee)}{\varepsilon(\mu\mu)}\cdot\frac{1}{r_{J/\psi}}$')
        plt.tight_layout()
        plt.grid()
        plt.savefig(f'{self._out_dir}/average_{preffix}.png')
        plt.close('all')
    #----------------------------------------
    def _average(self, arr_ck, cov, preffix=None):
        ck_val, ck_var = jac.propagate(lambda x : sum(x)/len(x), arr_ck, cov)
        ck_val, ck_var = float(ck_val), float(ck_var)

        ck_err = math.sqrt(ck_var)
        self._plot_avg(mu=ck_val, sg=ck_err, arr=arr_ck, mat=cov, preffix=preffix)

        return ck_val, ck_var
    #----------------------------------------
    def get_combination(self, add_tis=True):
        '''
        Parameters
        ------------
        add_tis (bool): If true, will return TIS ck and 2x2 covariance, if false, TIS is dropped

        Returns
        ------------
        Tuple with dictionaries with the rjpsi and efficiencies, e.g:

        d_rjpsi, d_eff, cov = cmb.get_cobination()

        the values of the first two dictionaries themselves are not meaningful, but when used
        to calculate ck, they should provide the right combined value
        '''
        self._initialize()

        arr_ck_tos, arr_ck_tis = self._get_ck()
        cov_tos = self._get_cov(trig='TOS') 
        cov_tis = self._get_cov(trig='TIS')

        ck_val_tos, ck_var_tos = self._average(arr_ck_tos, cov_tos, preffix='tos')
        ck_val_tis, ck_var_tis = self._average(arr_ck_tis, cov_tis, preffix='tis')

        eff_val = 1 - 1e-6
        if add_tis:
            d_rjpsi = {'all_TOS' : 1., 'all_TIS' : 1.}
            d_eff   = {'all_TOS' : (eff_val, ck_val_tos), 'all_TIS' : (eff_val, ck_val_tis) }
            cov     = [[ck_var_tos, 0], [0, ck_var_tis]]
        else:
            d_rjpsi = {'all_TOS' : 1.}
            d_eff   = {'all_TOS' : (eff_val, ck_val_tos)}
            cov     = [[ck_var_tos]]

        return d_rjpsi, d_eff, numpy.array(cov)
#----------------------------------------

