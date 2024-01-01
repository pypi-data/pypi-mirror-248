from model_analyzer import analyzer as mana

import zfit

#---------------------------------------------
def delete_all_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#---------------------------------------------
def get_model():
    obs          = zfit.Space('x', limits=(-10, 10))
    mu           = zfit.Parameter("mu", 2.4, -1, 5)
    sg           = zfit.Parameter("sg", 1.3,  0, 5)
    ne           = zfit.Parameter('ne', 100, 0, 1000)
    gauss        = zfit.pdf.Gauss(obs=obs, mu=mu, sigma=sg)

    return gauss.create_extended(ne) 
#---------------------------------------------
def test_speed():
    model = get_model()
    
    obj   =mana(pdf=model)
    obj.out_dir = 'tests/model_analyzer/speed'
    obj.speed(nfit=10)

    delete_all_pars()
#---------------------------------------------
def test_pulls():
    model = get_model()
    
    obj   =mana(pdf=model)
    obj.out_dir = 'tests/model_analyzer/pulls'
    obj.pulls(nfit=10)

    delete_all_pars()
#---------------------------------------------
def main():
    #test_speed()
    test_pulls()
#---------------------------------------------
if __name__ == '__main__':
    main()

