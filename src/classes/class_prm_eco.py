class prm_eco:
# --------------------- Constructor ----------------------------------------------------------------------------------    
    def __init__(self, r, ct=1, dt=1, occ=0, fix_om=0, fix_mi = 0, var_om=0, var_f=0, var_co2=0, var_mi=0):
        self._r   = r    # Discount rate
        self._ct  = ct   # Construction Time [y]
        self._dt  = dt   # Depreciation Time [y]
        self._occ = occ  # Overnight Construction Cost [M€/MW]
        self._fix_om  = fix_om  # Fix OM cost [€/MW]
        self._fix_mi  = fix_mi  # Misc Fix cost [€/MW] => Sum of other fixed costs
        self._var_om  = var_om   # var OM cost [€/MWh ouput]
        self._var_f   = var_f    # var fuel cost [€/MWh input]
        self._var_co2 = var_co2  # var carbon cost [€/MWh i]
        self._var_mi  = var_mi   # Misc var [€/MWh i] => Sum of other variable costs
        self._tic  = self.calculate_tic()  # Total Investment Costs [€/MW]
        self._idc  = self.calculate_idc()  # Interest During Construction [€/MW]
        self._fix_acap = self.calculate_fix_acap() # Annual CAPEX [€/MW/y]

# --------------------- End Of Constructor ---------------------------------------------------------------------------    

    # Calculate Total Investment Cost
    def calculate_tic(self):
        # Source : Haeseleer (2013) p39 (!! bracket error => IDC = TIC - OCC !!)
        # And Considering uniform construction cost profile to simplify...
        return self._occ / self._ct * ( (1 + self._r) / self._r ) * ( (1 + self._r)**self._ct - 1)
    
    # Calculate Interest During Construction Costs
    def calculate_idc(self):
        return self._tic - self._occ

    # Calculate Annual CAPEX cost
    def calculate_fix_acap(self):
        # Source : Footnote Hansen & Percebois - Energie pXX
        return self._tic * ( (self._r*(1+self._r)**self._dt) / ((1+self._r)**self._dt - 1) ) 
    
# --------------------- GET/SET methods -------------------------------------------------------------------------------

    # Get methods
    def get_r(self):
        return self._r
    def get_ct(self):
        return self._ct
    def get_dt(self):
        return self._dt
    def get_occ(self):
        return self._occ
    def get_fix_om(self):
        return self._fix_om
    def get_fix_mi(self):
        return self._fix_mi
    def get_var_om(self):
        return self._var_om
    def get_var_f(self):
        return self._var_f
    def get_var_co2(self):
        return self._var_co2
    def get_var_mi(self):
        return self._var_mi
    def get_fix_tot(self):
        return self._fix_acap + self._fix_om + self._fix_mi
    def get_var_tot(self):
        return self._var_om + self._var_f + self._var_co2 + self._var_mi
    def get_cost_profile(self):
        U = np.arange(1, 8761, 1)
        return self._fix_acap + self._fix_om + self._fix_mi + (self._var_om + self._var_f + self._var_co2 + self._var_mi) * U
    
    # Set methods
    def set_r(self, r):
        self._r = r
        # Recalculate IDC after updating cash_flows
        self._tic  = self.calculate_tic()
        self._idc  = self.calculate_idc()
        self._fix_acap = self.calculate_fix_acap()

    def set_ct(self, ct):
        self._ct = ct
        # Recalculate IDC after updating cash_flows
        self._tic  = self.calculate_tic()
        self._idc  = self.calculate_idc()
        self._fix_acap = self.calculate_fix_acap()
    def set_dt(self, dt):
        self._dt = dt
        # Recalculate IDC after updating cash_flows
        self._tic  = self.calculate_tic()
        self._idc  = self.calculate_idc()
        self._fix_acap = self.calculate_fix_acap()
    def set_occ(self, occ):
        self._occ = occ
        # Recalculate IDC after updating cash_flows
        self._tic  = self.calculate_tic()
        self._idc  = self.calculate_idc()
        self._fix_acap = self.calculate_fix_acap()
    def set_fix_om(self, fix_om):
        self._fix_om = fix_om
    def set_fix_mi(self, fix_mi):
        self._fix_mi = fix_mi
    def set_var_om(self, var_om):
        self._var_om = var_om
    def set_var_f(self, var_f):
        self._var_f = var_f
    def set_var_co2(self, var_co2):
        self._var_co2 = var_co2
    def set_var_mi(self, var_mi):
        self._var_mi = var_mi

# --------------------- PRINT methods ---------------------------------------------------------------------------------

    def Print(self):
        print()
        print('--------------------------------------------')
        print('--- Eco parameters -------------------------')
        print('--------------------------------------------')
        print(f"discount rate : {self._r}")
        print('--------------------------------------------')
        print(f"construction time : {self._ct} y")
        print(f"depreciation time : {self._dt} y ")
        print('--------------------------------------------')
        print(f"Overnight Construction Cost :  {self._occ} M€/MW")
        print(f" -> Interest During Construction : {self._idc} M€/MW")
        print(f" -> Total Investment Costs :       {self._tic} M€/MW")
        print(f" -> Annual CAPEX :                 {self._fix_acap} M€/MW/y")
        print('--------------------------------------------')
        print(f"fix_om:  {self._fix_om} M€/MW/y")
        print(f"var_om:  {self._var_om} M€/MWh")
        print(f"var_f:   {self._var_f} M€/MWhi")
        print(f"var_co2: {self._var_co2} M€/MWh")
        print('--------------------------------------------')
        print()
    
