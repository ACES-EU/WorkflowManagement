import pandapower as pp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.DataFrame()
dfminat = pd.DataFrame()
dfmaxat = pd.DataFrame()
dfbus = pd.DataFrame()

for i in range(0, 9):
    for p in np.arange(0, 3000, 10):
        net = pp.create_empty_network()

        print(i)
        print(p)
        load = [11, 11, 38, 35, 13, 18, 40, 37, 40]
        load[i] = p
        ###############################
        # Beginning of Configuration
        ###############################

        ###############################
        # Buses
        Lavrio400 = pp.create_bus(net, name="Lavrio400", vn_kv=400)  # 0
        Lavrio150 = pp.create_bus(net, name="Lavrio150", vn_kv=150)  # 1

        SYROSP40 = pp.create_bus(net, name="SYROSP40", vn_kv=150)  # 2
        SYROSP70 = pp.create_bus(net, name="SYROSP70", vn_kv=150)  # 3
        PAROSP10 = pp.create_bus(net, name="PAROSP10", vn_kv=150)  # 4

        MOLAOI_TR1 = pp.create_bus(net, name='MOLAOI_TR1  ', vn_kv=150)  # 5
        MOLAOI_TR2 = pp.create_bus(net, name='MOLAOI_TR2  ', vn_kv=150)  # 6

        CHANIA1_A = pp.create_bus(net, name='CHANIA1_A', vn_kv=150)  # 7
        CHANIA1_B = pp.create_bus(net, name='CHANIA1_B', vn_kv=150)  # 8
        CHANIA1_MT = pp.create_bus(net, name='CHANIA1_MT  ', vn_kv=21)  # 9
        CHANIA2 = pp.create_bus(net, name='CHANIA2     ', vn_kv=150)  # 10
        CHANIA2_MT = pp.create_bus(net, name='CHANIA2_MT  ', vn_kv=21)  # 11

        AGIA = pp.create_bus(net, name='AGIA        ', vn_kv=150)  # 12
        KASTELI = pp.create_bus(net, name='KASTELI     ', vn_kv=150)  # 13

        # Shunt buses
        LS40_R = pp.create_bus(net, name="LavrioSyros40_R", vn_kv=150)  # 14
        S40L_R = pp.create_bus(net, name="Syros40Lavrio_R", vn_kv=150)  # 15
        LS70_R = pp.create_bus(net, name="LavrioSyros70_R", vn_kv=150)  # 16
        S70L_R = pp.create_bus(net, name="Syros70Lavrio_R", vn_kv=150)  # 17

        SP_R = pp.create_bus(net, name="SyrosParos_R", vn_kv=150)  # 18
        PS_R = pp.create_bus(net, name="ParosSyros_R", vn_kv=150)  # 19

        MTR1CH1_A_R = pp.create_bus(net, name="MolaoiTR1-Chania1A_R", vn_kv=150)  # 20
        CH1_AMTR1_R = pp.create_bus(net, name="Chania1A-MolaoiTR1_R", vn_kv=150)  # 21
        MTR2CH1_B_R = pp.create_bus(net, name="MolaoiTR2-Chania1B_R", vn_kv=150)  # 22
        CH1_BMTR2_R = pp.create_bus(net, name="Chania1B-MolaoiTR2_R", vn_kv=150)  # 23

        ###############################
        # External - Slack Bus
        ###############################

        pp.create_ext_grid(net, Lavrio400)
        pp.create_ext_grid(net, MOLAOI_TR1)

        ###############################
        # Transformers
        ###############################

        # LAVRIO400-LAVRIO150
        T1 = pp.create_transformer_from_parameters(net, hv_bus=Lavrio400, lv_bus=Lavrio150, name="Trafo1", sn_mva=280,
                                                   vn_hv_kv=400, vn_lv_kv=150, vk_percent=10.2, vkr_percent=0.2,
                                                   pfe_kw=30, i0_percent=0, shift_degree=0)
        T2 = pp.create_transformer_from_parameters(net, hv_bus=Lavrio400, lv_bus=Lavrio150, name="Trafo2", sn_mva=280,
                                                   vn_hv_kv=400, vn_lv_kv=150, vk_percent=10.2, vkr_percent=0.2,
                                                   pfe_kw=30, i0_percent=0, shift_degree=0)

        # LAVRIO400-MOLAOI
        T3 = pp.create_transformer_from_parameters(net, hv_bus=Lavrio400, lv_bus=MOLAOI_TR1, name="Trafo3", sn_mva=280,
                                                   vn_hv_kv=400, vn_lv_kv=150, vk_percent=10.2, vkr_percent=0.2,
                                                   pfe_kw=30, i0_percent=0, shift_degree=0)
        T4 = pp.create_transformer_from_parameters(net, hv_bus=Lavrio400, lv_bus=MOLAOI_TR2, name="Trafo4", sn_mva=280,
                                                   vn_hv_kv=400, vn_lv_kv=150, vk_percent=10.2, vkr_percent=0.2,
                                                   pfe_kw=30, i0_percent=0, shift_degree=0)

        # #CHANIA1 - CHANIA1_MT
        T5 = pp.create_transformer_from_parameters(net, hv_bus=CHANIA1_A, lv_bus=CHANIA1_MT, name="Trafo5", sn_mva=100,
                                                   vn_hv_kv=150, vn_lv_kv=21, vk_percent=10.2, vkr_percent=0.2,
                                                   pfe_kw=30, i0_percent=0, shift_degree=0)
        # #CHANIA2 - CHANIA2_MT
        T6 = pp.create_transformer_from_parameters(net, hv_bus=CHANIA2, lv_bus=CHANIA2_MT, name="Trafo6", sn_mva=100,
                                                   vn_hv_kv=150, vn_lv_kv=21, vk_percent=10.2, vkr_percent=0.2,
                                                   pfe_kw=30, i0_percent=0, shift_degree=0)

        ###############################
        # Lines
        ###############################

        lineLS1 = pp.create_line_from_parameters(net, from_bus=LS40_R, to_bus=S40L_R, length_km=106.8,
                                                 r_ohm_per_km=0.02976, x_ohm_per_km=0.05653, c_nf_per_km=1.3747,
                                                 max_i_ka=0.7701852591)
        lineLS2 = pp.create_line_from_parameters(net, from_bus=LS70_R, to_bus=S70L_R, length_km=106.8,
                                                 r_ohm_per_km=0.02976, x_ohm_per_km=0.05653, c_nf_per_km=1.3747,
                                                 max_i_ka=0.76980035892)
        lineSP = pp.create_line_from_parameters(net, from_bus=SP_R, to_bus=PS_R, length_km=47.53, r_ohm_per_km=0.02108,
                                                x_ohm_per_km=0.03182, c_nf_per_km=0.47674, max_i_ka=0.54001495178)
        lineMTR1CH1_A = pp.create_line_from_parameters(net, from_bus=MTR1CH1_A_R, to_bus=CH1_AMTR1_R, length_km=180,
                                                       r_ohm_per_km=0.04438, x_ohm_per_km=0.11293, c_nf_per_km=2.60972,
                                                       max_i_ka=0.7701852591)
        lineMTR2CH1_B = pp.create_line_from_parameters(net, from_bus=MTR2CH1_B_R, to_bus=CH1_BMTR2_R, length_km=180,
                                                       r_ohm_per_km=0.04438, x_ohm_per_km=0.11293, c_nf_per_km=2.60972,
                                                       max_i_ka=0.7701852591)
        lineCH1_ACH2 = pp.create_line_from_parameters(net, from_bus=CHANIA1_A, to_bus=CHANIA2, length_km=5,
                                                      r_ohm_per_km=0.001110, x_ohm_per_km=0.004470,
                                                      c_nf_per_km=0.065030, max_i_ka=0.7701852591)
        lineCH1_BCH2 = pp.create_line_from_parameters(net, from_bus=CHANIA2, to_bus=CHANIA1_B, length_km=5,
                                                      r_ohm_per_km=0.001110, x_ohm_per_km=0.004470,
                                                      c_nf_per_km=0.065030, max_i_ka=0.7701852591)
        lineCH1_BAG = pp.create_line_from_parameters(net, from_bus=CHANIA1_B, to_bus=AGIA, length_km=10,
                                                     r_ohm_per_km=0.004330, x_ohm_per_km=0.018750, c_nf_per_km=0.006160,
                                                     max_i_ka=0.7701852591)
        lineAGKAST = pp.create_line_from_parameters(net, from_bus=AGIA, to_bus=KASTELI, length_km=22.5,
                                                    r_ohm_per_km=0.009740, x_ohm_per_km=0.042190, c_nf_per_km=0.013860,
                                                    max_i_ka=0.7701852591)

        # Bus to bus
        lineSS = pp.create_line_from_parameters(net, from_bus=SYROSP40, to_bus=SYROSP70, length_km=1, r_ohm_per_km=0,
                                                x_ohm_per_km=0.001, c_nf_per_km=0, max_i_ka=38.486168944)
        lineMTR1MTR2 = pp.create_line_from_parameters(net, from_bus=MOLAOI_TR1, to_bus=MOLAOI_TR2, length_km=1,
                                                      r_ohm_per_km=0, x_ohm_per_km=0.001, c_nf_per_km=0,
                                                      max_i_ka=38.486168944)
        lineCH1_ACH1_B = pp.create_line_from_parameters(net, from_bus=CHANIA1_A, to_bus=CHANIA1_B, length_km=1,
                                                        r_ohm_per_km=0, x_ohm_per_km=0.001, c_nf_per_km=0,
                                                        max_i_ka=38.486168944)

        # Shunt Bus lines
        lineLS40_R = pp.create_line_from_parameters(net, from_bus=Lavrio150, to_bus=LS40_R, length_km=1, r_ohm_per_km=0,
                                                    x_ohm_per_km=0.001, c_nf_per_km=0, max_i_ka=38.486168944)
        lineLS70_R = pp.create_line_from_parameters(net, from_bus=Lavrio150, to_bus=LS70_R, length_km=1, r_ohm_per_km=0,
                                                    x_ohm_per_km=0.001, c_nf_per_km=0, max_i_ka=38.486168944)

        lineS40L_R = pp.create_line_from_parameters(net, from_bus=S40L_R, to_bus=SYROSP40, length_km=1, r_ohm_per_km=0,
                                                    x_ohm_per_km=0.001, c_nf_per_km=0, max_i_ka=38.486168944)
        lineS70L_R = pp.create_line_from_parameters(net, from_bus=S70L_R, to_bus=SYROSP70, length_km=1, r_ohm_per_km=0,
                                                    x_ohm_per_km=0.001, c_nf_per_km=0, max_i_ka=38.486168944)

        lineSP_R = pp.create_line_from_parameters(net, from_bus=SYROSP70, to_bus=SP_R, length_km=1, r_ohm_per_km=0,
                                                  x_ohm_per_km=0.001, c_nf_per_km=0, max_i_ka=38.486168944)
        linePS_R = pp.create_line_from_parameters(net, from_bus=PS_R, to_bus=PAROSP10, length_km=1, r_ohm_per_km=0,
                                                  x_ohm_per_km=0.001, c_nf_per_km=0, max_i_ka=38.486168944)

        lineMTR1CH1_A_R = pp.create_line_from_parameters(net, from_bus=MOLAOI_TR1, to_bus=MTR1CH1_A_R, length_km=1,
                                                         r_ohm_per_km=0, x_ohm_per_km=0.001, c_nf_per_km=0,
                                                         max_i_ka=38.486168944)
        lineCH1_AMTR1_R = pp.create_line_from_parameters(net, from_bus=CHANIA1_A, to_bus=CH1_AMTR1_R, length_km=1,
                                                         r_ohm_per_km=0, x_ohm_per_km=0.001, c_nf_per_km=0,
                                                         max_i_ka=38.486168944)

        lineMTR2CH1_B_R = pp.create_line_from_parameters(net, from_bus=MOLAOI_TR2, to_bus=MTR2CH1_B_R, length_km=1,
                                                         r_ohm_per_km=0, x_ohm_per_km=0.001, c_nf_per_km=0,
                                                         max_i_ka=38.486168944)
        lineCH1_BMTR2_R = pp.create_line_from_parameters(net, from_bus=CHANIA1_B, to_bus=CH1_BMTR2_R, length_km=1,
                                                         r_ohm_per_km=0, x_ohm_per_km=0.001, c_nf_per_km=0,
                                                         max_i_ka=38.486168944)

        ###############################
        # Switches
        ###############################

        # BUS TO LINE SWITCHES
        # swL1S	= pp.create_switch(net,	Lavrio150,	lineLS40_R,		et="l",		type="CB",		closed=True)
        # swSL1	= pp.create_switch(net,	SYROSP40,	lineS40L_R,		et="l",		type="CB",		closed=True)
        # swL2S	= pp.create_switch(net,	Lavrio150,	lineLS70_R,		et="l",		type="CB",		closed=True)
        # swSL2	= pp.create_switch(net,	SYROSP70,	lineS70L_R,		et="l",		type="CB",		closed=True)
        # swSP	= pp.create_switch(net,	SYROSP70,	lineSP_R,		et="l",		type="CB",		closed=True)
        # swPS	= pp.create_switch(net,	PAROSP10,	linePS_R,		et="l",		type="CB",		closed=True)

        # BUS to BUS switches
        # swSS	     = pp.create_switch(net,	SYROSP40,	   lineSS,   	        et="l",		type="CB",		closed=True)
        # swMTR1MTR2   = pp.create_switch(net,	MOLAOI_TR1,	   lineMTR1MTR2,       	et="l",		type="CB",		closed=True)
        # swCH1_ACH1_B = pp.create_switch(net,	CHANIA1_A,	   lineCH1_ACH1_B,   	et="l",		type="CB",		closed=True)

        # swLMTR2 = pp.create_switch(net,	CHANIA1_A,	   lineCH1_ACH1_B,   	et="l",		type="CB",		closed=True)

        # swMTR1CH1_A  = pp.create_switch(net,	MOLAOI_TR1,	lineMTR1CH1_A_R,		et="l",		type="CB",		closed=True)
        # swCH1_AMTR1  = pp.create_switch(net,	CHANIA1_A,	lineCH1_AMTR1_R,		et="l",		type="CB",		closed=True)
        # swMTR2CH1_B  = pp.create_switch(net,	MOLAOI_TR2,	lineMTR2CH1_B_R,		et="l",		type="CB",		closed=True)
        # swCH1_BMTR2  = pp.create_switch(net,	CHANIA1_B,	lineCH1_BMTR2_R,		et="l",		type="CB",		closed=True)

        # swCH1_BCH2   = pp.create_switch(net,	CHANIA1_B,	lineCH1_BCH2,		et="l",		type="CB",		closed=True)
        # swCH1_BAG    = pp.create_switch(net,	CHANIA1_B,	lineCH1_BAG,		et="l",		type="CB",		closed=True)
        # swAGKAST     = pp.create_switch(net,	AGIA,	     lineAGKAST,		et="l",		type="CB",		closed=True)

        ###############################
        # Load MAX
        ###############################

        LOAD_SYROSP40 = pp.create_load(net, SYROSP40, name="LOAD_SYROSP40", p_mw=load[0], q_mvar=load[0] * 0.4)
        LOAD_SYROSP70 = pp.create_load(net, SYROSP70, name="LOAD_SYROSP70", p_mw=load[1], q_mvar=load[1] * 0.4)
        LOAD_PAROS_1 = pp.create_load(net, PAROSP10, name="LOAD_PAROS_1", p_mw=load[2], q_mvar=load[2] * 0.4)
        LOAD_PAROS_2 = pp.create_load(net, PAROSP10, name="LOAD_PAROS_2", p_mw=load[3], q_mvar=load[3] * 0.4)
        LOAD_LAVRIO_1 = pp.create_load(net, Lavrio150, name="LOAD_LAVRIO_1", p_mw=load[4], q_mvar=load[4] * 0.4)
        LOAD_LAVRIO_2 = pp.create_load(net, Lavrio150, name="LOAD_LAVRIO_2", p_mw=load[5], q_mvar=load[5] * 0.4)
        LOAD_CHANIA1_MT = pp.create_load(net, CHANIA1_MT, name="LOAD_CHANIA1_MT", p_mw=load[6], q_mvar=load[6] * 0.4)
        LOAD_CHANIA2_MT = pp.create_load(net, CHANIA2_MT, name="LOAD_CHANIA2_MT", p_mw=load[7], q_mvar=load[7] * 0.4)
        LOAD_KASTELI = pp.create_load(net, KASTELI, name="LOAD_KASTELI", p_mw=load[8], q_mvar=load[8] * 0.4)
        ###############################
        # Generators
        ###############################

        CRETE_Gen = pp.create_gen(net, CHANIA1_A, name="Crete_Gen", p_mw=226.000, min_p_mw=0, max_p_mw=300,
                                  min_q_mvar=0, max_q_mvar=413.512)

        # SVC
        SYROS_SVC = pp.create_gen(net, SYROSP40, name="SYROS_SVC", p_mw=0, min_p_mw=0, max_p_mw=0, min_q_mvar=-100,
                                  max_q_mvar=100)

        # ASP
        SyrosASP = pp.create_gen(net, SYROSP70, name="SyrosASP", p_mw=12.068, min_p_mw=0, max_p_mw=45.04, min_q_mvar=0,
                                 max_q_mvar=113.512)
        ParosASP = pp.create_gen(net, PAROSP10, name="ParosASP", p_mw=37.039, min_p_mw=0, max_p_mw=91.85, min_q_mvar=0,
                                 max_q_mvar=27.356)

        # #DER
        # ParosKamares	= pp.create_gen(net,	PAROSP10,		name="ParosKamares",	p_mw=3.0,	min_p_mw=0,		max_p_mw=3.0,		min_q_mvar=0,		max_q_mvar=0)

        # #Storage
        # ParosStorage    = pp.create_storage(net,    PAROSP10,       p_mw=10,     max_e_mwh=5.5)

        ###############################
        # Shunts
        ###############################

        pp.create_shunt(net, PAROSP10, 25)

        pp.create_shunt(net, SP_R, -16)
        pp.create_shunt(net, PS_R, -16)
        pp.create_shunt(net, CHANIA1_A, 16)
        pp.create_shunt(net, CHANIA1_MT, 16)
        pp.create_shunt(net, CHANIA2_MT, 16)
        pp.create_shunt(net, CHANIA2, 16)
        pp.create_shunt(net, AGIA, 16)
        pp.create_shunt(net, KASTELI, 16)

        pp.create_shunt(net, S40L_R, -50)
        pp.create_shunt(net, S70L_R, -50)
        pp.create_shunt(net, LS40_R, -50)
        pp.create_shunt(net, LS70_R, -50)

        pp.create_shunt(net, MTR1CH1_A_R, -120)
        pp.create_shunt(net, CH1_AMTR1_R, -120)
        pp.create_shunt(net, MTR2CH1_B_R, -120)
        pp.create_shunt(net, CH1_BMTR2_R, -120)

        ###############################
        # End of Configuration
        ###############################

        # pp.runpp(net, "nr", enforce_q_lims=True)

        ###############################
        # OpenFlow
        ###############################

        # pp.runpp(net, "nr", enforce_q_lims=True)
        try:
            pp.runpp(net, "nr")
        except:
            print('error')

        from pandapower.plotting import pf_res_plotly

        # pf_res_plotly(net)

        # print("\n#########################################################\n")
        # print(net.res_bus)
        # print("\n#########################################################\n")
        # print(net.res_line)
        # print("\n#########################################################\n")
        # print(net.res_trafo)
        # print("\n#########################################################\n")
        # print(net.res_load)
        # print("\n#########################################################\n")
        # print(net.res_gen)
        # print("\n#########################################################\n")
        # print(net.res_storage)
        # print("\n#########################################################\n")

        try:
            pp.runpp(net, "nr")
        except:
            print('error')
        print(net.res_bus)
        df[str(i) + '_' + str(p)] = net.res_bus["vm_pu"]
        # dfmin[str(i)+'_'+str(p)]=min(net.res_bus["vm_pu"])
        # dfmax[str(i)+'_'+str(p)]=max(net.res_bus["vm_pu"])

        dfminat.at[str(i), str(p)] = min(net.res_bus["vm_pu"])
        dfmaxat.at[str(i), str(p)] = max(net.res_bus["vm_pu"])
        dfbus.at[str(i), str(p)] = net.res_bus["vm_pu"][1]

# dfmin.to_excel('min output.xlsx')

fig, ax = plt.subplots()
sns.heatmap(dfminat, annot=False, ax=ax)
fig.savefig("output/Load sensitivity heatmap - min.png")

fig, ax = plt.subplots()
sns.heatmap(dfmaxat, annot=False, ax=ax)
fig.savefig("output/Load sensitivity heatmap - max.png")

fig, ax = plt.subplots()
sns.heatmap(dfbus, annot=False, ax=ax)
fig.savefig("output/Load sensitivity heatmap - bus1.png")

df.to_excel('output/bus voltage for different scenarios.xlsx')
dfminat.to_excel('output/min voltage for different loads.xlsx')
dfmaxat.to_excel('output/max voltage for different loads.xlsx')


