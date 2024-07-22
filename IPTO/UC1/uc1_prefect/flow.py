import numpy as np

from prefect import flow, get_run_logger, task

from load_sensitivity import init_dfs, empty_network, init_buses, init_transformers, make_lines, load_max, \
    make_generators, make_shunts, simulate, make_figures


@task
def set_dfs():
    df, dfminat, dfmaxat, dfbus = init_dfs()
    return df, dfminat, dfmaxat, dfbus


@task
def set_empty_network(i, p):
    net, load = empty_network(i, p)
    return net, load


@task
def set_net_buses(net):
    net, Lavrio400, Lavrio150, SYROSP40, SYROSP70, PAROSP10, MOLAOI_TR1, MOLAOI_TR2, \
        CHANIA1_A, CHANIA1_B, CHANIA1_MT, CHANIA2, CHANIA2_MT, AGIA, KASTELI, LS40_R, \
        S40L_R, LS70_R, S70L_R, SP_R, PS_R, \
        MTR1CH1_A_R, CH1_AMTR1_R, MTR2CH1_B_R, CH1_BMTR2_R = init_buses(net)

    return net, Lavrio400, Lavrio150, SYROSP40, SYROSP70, PAROSP10, MOLAOI_TR1, MOLAOI_TR2, \
        CHANIA1_A, CHANIA1_B, CHANIA1_MT, CHANIA2, CHANIA2_MT, AGIA, KASTELI, LS40_R, \
        S40L_R, LS70_R, S70L_R, SP_R, PS_R, MTR1CH1_A_R, CH1_AMTR1_R, MTR2CH1_B_R, CH1_BMTR2_R


@task
def set_transformers(
        net,
        Lavrio400, Lavrio150,
        MOLAOI_TR1, MOLAOI_TR2,
        CHANIA1_A, CHANIA1_MT,
        CHANIA2, CHANIA2_MT
):
    T1, T2, T3, T4, T5, T6 = init_transformers(
        net,
        Lavrio400, Lavrio150,
        MOLAOI_TR1, MOLAOI_TR2,
        CHANIA1_A, CHANIA1_MT,
        CHANIA2, CHANIA2_MT
    )
    return T1, T2, T3, T4, T5, T6


@task
def set_net_lines(
        net, LS40_R, S40L_R, LS70_R, S70L_R,
        SP_R, PS_R, CH1_AMTR1_R, MTR1CH1_A_R, CH1_BMTR2_R, MTR2CH1_B_R,
        CHANIA1_A, CHANIA2, CHANIA1_B, AGIA, KASTELI, SYROSP40, SYROSP70, MOLAOI_TR1,
        MOLAOI_TR2, Lavrio150, PAROSP10
):
    lineLS1, lineLS2, lineSP, lineMTR1CH1_A, lineMTR2CH1_B, lineCH1_ACH2, lineCH1_BCH2, lineCH1_BAG, \
        lineCH1_BAG, lineSS, lineMTR1MTR2, lineCH1_ACH1_B, lineLS40_R, lineLS70_R, lineS40L_R, lineS70L_R, \
        lineSP_R, linePS_R, lineMTR1CH1_A_R, lineCH1_AMTR1_R, \
        lineMTR2CH1_B_R, lineCH1_BMTR2_R, lineAGKAST = make_lines(
        net, LS40_R, S40L_R, LS70_R, S70L_R,
        SP_R, PS_R, CH1_AMTR1_R, MTR1CH1_A_R, CH1_BMTR2_R, MTR2CH1_B_R,
        CHANIA1_A, CHANIA2, CHANIA1_B, AGIA, KASTELI, SYROSP40, SYROSP70, MOLAOI_TR1,
        MOLAOI_TR2, Lavrio150, PAROSP10)
    return lineLS1, lineLS2, lineSP, lineMTR1CH1_A, lineMTR2CH1_B, lineCH1_ACH2, lineCH1_BCH2, lineCH1_BAG, \
        lineCH1_BAG, lineSS, lineMTR1MTR2, lineCH1_ACH1_B, lineLS40_R, lineLS70_R, lineS40L_R, lineS70L_R, \
        lineSP_R, linePS_R, lineMTR1CH1_A_R, lineCH1_AMTR1_R, lineMTR2CH1_B_R, lineCH1_BMTR2_R, lineAGKAST


@task
def set_load_max(
        net, SYROSP40, SYROSP70, load, PAROSP10,
        Lavrio150, CHANIA1_MT, CHANIA2_MT, KASTELI
):
    LOAD_SYROSP40, LOAD_SYROSP70, LOAD_PAROS_1, LOAD_PAROS_2, LOAD_LAVRIO_1, LOAD_LAVRIO_2, LOAD_CHANIA1_MT, \
        LOAD_CHANIA2_MT, LOAD_KASTELI = load_max(
        net, SYROSP40, SYROSP70, load, PAROSP10, Lavrio150, CHANIA1_MT, CHANIA2_MT, KASTELI
    )
    return LOAD_SYROSP40, LOAD_SYROSP70, LOAD_PAROS_1, LOAD_PAROS_2, LOAD_LAVRIO_1, LOAD_LAVRIO_2, LOAD_CHANIA1_MT, \
        LOAD_CHANIA2_MT, LOAD_KASTELI


@task
def set_gens(
        net, CHANIA1_A, SYROSP40,
        SYROSP70, PAROSP10
):
    CRETE_Gen, SYROS_SVC, SyrosASP, ParosASP = make_generators(
        net, CHANIA1_A, SYROSP40,
        SYROSP70, PAROSP10
    )
    return CRETE_Gen, SYROS_SVC, SyrosASP, ParosASP


@task
def set_net_shunts(
        net, PAROSP10, SP_R, CHANIA1_A,
        PS_R, CHANIA1_MT, CHANIA2_MT, CHANIA2, AGIA, KASTELI, S40L_R,
        S70L_R, LS40_R, LS70_R, MTR1CH1_A_R, CH1_AMTR1_R, MTR2CH1_B_R,
        CH1_BMTR2_R
):
    net = make_shunts(
        net, PAROSP10, SP_R, CHANIA1_A,
        PS_R, CHANIA1_MT, CHANIA2_MT, CHANIA2, AGIA, KASTELI, S40L_R,
        S70L_R, LS40_R, LS70_R, MTR1CH1_A_R, CH1_AMTR1_R, MTR2CH1_B_R,
        CH1_BMTR2_R
    )
    return net


@task
def make_simulation(
        i, p,
        net, df, dfminat,
        dfmaxat, dfbus
):
    df, dfminat, dfmaxat, dfbus = simulate(
        i, p,
        net, df, dfminat,
        dfmaxat, dfbus
    )
    return df, dfminat, dfmaxat, dfbus


def create_figures(df, dfminat, dfmaxat, dfbus):
    make_figures(df, dfminat, dfmaxat, dfbus)


@flow
def uc1_load_sens():
    df, dfminat, dfmaxat, dfbus = set_dfs()

    for i in range(0, 9):
        for p in np.arange(0, 3000, 100):
            net, load = set_empty_network(i, p)

            net, Lavrio400, Lavrio150, SYROSP40, SYROSP70, PAROSP10, MOLAOI_TR1, MOLAOI_TR2, \
                CHANIA1_A, CHANIA1_B, CHANIA1_MT, CHANIA2, CHANIA2_MT, AGIA, KASTELI, LS40_R, \
                S40L_R, LS70_R, S70L_R, SP_R, PS_R, \
                MTR1CH1_A_R, CH1_AMTR1_R, MTR2CH1_B_R, CH1_BMTR2_R = set_net_buses(net)

            T1, T2, T3, T4, T5, T6 = set_transformers(
                net, Lavrio400, Lavrio150, MOLAOI_TR1, MOLAOI_TR2,
                CHANIA1_A, CHANIA1_MT, CHANIA2, CHANIA2_MT)

            lineLS1, lineLS2, lineSP, lineMTR1CH1_A, lineMTR2CH1_B, lineCH1_ACH2, lineCH1_BCH2, lineCH1_BAG, \
                lineCH1_BAG, lineSS, lineMTR1MTR2, lineCH1_ACH1_B, lineLS40_R, lineLS70_R, lineS40L_R, lineS70L_R, \
                lineSP_R, linePS_R, lineMTR1CH1_A_R, lineCH1_AMTR1_R, \
                lineMTR2CH1_B_R, lineCH1_BMTR2_R, lineAGKAST = set_net_lines(
                net, LS40_R, S40L_R, LS70_R, S70L_R,
                SP_R, PS_R, CH1_AMTR1_R, MTR1CH1_A_R, CH1_BMTR2_R, MTR2CH1_B_R,
                CHANIA1_A, CHANIA2, CHANIA1_B, AGIA, KASTELI, SYROSP40, SYROSP70, MOLAOI_TR1,
                MOLAOI_TR2, Lavrio150, PAROSP10)

            LOAD_SYROSP40, LOAD_SYROSP70, LOAD_PAROS_1, LOAD_PAROS_2, LOAD_LAVRIO_1, LOAD_LAVRIO_2, LOAD_CHANIA1_MT, \
                LOAD_CHANIA2_MT, LOAD_KASTELI = set_load_max(
                net, SYROSP40, SYROSP70, load, PAROSP10,
                Lavrio150, CHANIA1_MT, CHANIA2_MT, KASTELI
            )

            CRETE_Gen, SYROS_SVC, SyrosASP, ParosASP = set_gens(
                net, CHANIA1_A, SYROSP40,
                SYROSP70, PAROSP10
            )

            net = set_net_shunts(
                net, PAROSP10, SP_R, CHANIA1_A,
                PS_R, CHANIA1_MT, CHANIA2_MT, CHANIA2, AGIA, KASTELI, S40L_R,
                S70L_R, LS40_R, LS70_R, MTR1CH1_A_R, CH1_AMTR1_R, MTR2CH1_B_R,
                CH1_BMTR2_R
            )

            df, dfminat, dfmaxat, dfbus = make_simulation(
                i, p,
                net, df, dfminat,
                dfmaxat, dfbus
            )
            create_figures(df, dfminat, dfmaxat, dfbus)
