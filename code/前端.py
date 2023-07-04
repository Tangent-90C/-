import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import random
from matplotlib import pyplot as plt
import streamlit.components.v1 as components
from back_end import algebra
import sympy as sp
import numpy as np
from Domain import Domain


@st.cache_resource  # 不一定有必要缓存
def load_agb_sys():
    return algebra(Debug=True)


def load_定义域解析():
    return Domain()


st.set_page_config(page_title='智能代数系统', page_icon='🧮', layout='wide', initial_sidebar_state='auto')
tab1, tab2 = st.columns([1, 1])
agb = load_agb_sys()
domain_exp = load_定义域解析()
calc_finished = False

with tab1:
    t1, t2 = st.tabs(['代数', '定义新函数'])

    with t1:
        st.markdown('## 智能代数系统')
        if st.session_state.get('question') == None:
            agb.clear_var()
            agb.clear_diy_func()
        if st.session_state.get('submit_button'):
            question = st.text_input('请输入代数表达式：')
            if st.button('提交'):
                if question != st.session_state['question']:
                    agb.clear_var()
                st.session_state['question'] = question

            ans = agb(question)

            st.latex(ans)

            st.markdown('### 变量表')
            vars = agb.return_all_var()
            # 变为字典
            var_dict = {}
            # 给变量表中的变量赋值
            for var in vars:
                if st.session_state.get(f'{var}的值') is None:
                    st.session_state[f'{var}的值'] = float(random.randint(-5, 5))

                sli, d_v, min_start, max_end, d_step = st.columns([15, 3, 2, 2, 2])
                with d_v:
                    st.session_state[f'{var}的值'] = float(
                        st.text_input('值', value=st.session_state.get(f'{var}的值'), key=f'{var}的默认值'))
                with min_start:
                    min_v = float(st.text_input('最小值', value=-10.0, key=f'{var}的最小值'))
                with max_end:
                    max_v = float(st.text_input('最大值', value=10.0, key=f'{var}的最大值'))
                with d_step:
                    default_step = float(st.text_input('步长', value=0.1, key=f'{var}的步长'))
                with sli:
                    var_dict[var] = sp.Rational(
                        str(st.slider(f'{var}的数值', min_v, max_v, st.session_state[f'{var}的值'], default_step)))
                    st.session_state[f'{var}的值'] = var_dict[var].evalf()

            calc_finished = True

            st.markdown("带入上述变量后计算出的的值为：\n\n$$\n{}\n$$\n\n进一步计算得出的值为：\n\n$$\n{}\n$$".format(
                sp.latex(ans.subs(var_dict)), sp.latex(ans.subs(var_dict).evalf())))

        else:
            st.session_state['question'] = st.text_input('请输入代数表达式：')
            st.session_state['submit_button'] = st.button('提交')

    with t2:
        st.markdown('## 定义新函数')
        # 2个输入框，一个是新函数的名字，一个是新函数的表达式
        # 一个按钮，点击后将新函数的名字和表达式传入后端
        # 一个下拉框，显示所有已定义的函数，点击后将函数名传入后端，后端返回函数表达式，显示在下方

        一个参数的, 俩个参数的, 一个参数的可套娃的, 俩个参数的可套娃的 = st.tabs(
            ['一个参数的', '俩个参数的', '一个参数+可套娃的', '俩个参数+可套娃的'])
        with 一个参数的:
            f_name_c, f_vars, f_express_c = st.columns([2, 2, 6])
            with f_name_c:
                f_name = st.text_input('函数名', key='自定义的函数名_1变量', value='self_add')
            with f_vars:
                f_var = st.text_input('参数名', key='变量名_独', value='x')
            with f_express_c:
                f_express = st.text_input('函数表达式', key='一个变量的函数表达式', value="x + 1")
            if st.button('提交', key='一个变量的自定义函数的提交'):
                # 先判断有没有重名的函数
                if f_name in agb.return_all_func().keys():
                    st.error('函数名已存在！')
                else:
                    agb.define_new_func(f_name, f_express, var_list=[f_var])
                    st.success('函数定义成功！')

        with 俩个参数的:
            f_name_c, f_vars1, f_vars2, f_express_c = st.columns([2, 1, 1, 6])
            with f_name_c:
                f_name = st.text_input('函数名', key='函数名', value='add')
            with f_vars1:
                f_var_1 = st.text_input('参数名1', key='变量名1', value='x')
            with f_vars2:
                f_var_2 = st.text_input('参数名2', key='变量名2', value='y')
            with f_express_c:
                f_express = st.text_input('函数表达式', key='俩个变量的函数表达式', value="x + y")
            if st.button('提交', key='俩个变量自定义函数的提交'):
                if f_name in agb.return_all_func().keys():
                    st.error('函数名已存在！')
                else:
                    agb.define_new_func(f_name, f_express, var_list=[f_var_1, f_var_2])
                    st.success('函数定义成功！')

        with 一个参数的可套娃的:
            # 一个分段函数，要求给如一个分段函数，与每个分段点定义域
            st.markdown('# 别用，还没写完')
            f_name_c, f_vars1, f_vars2, f_分段 = st.columns([2, 1, 1, 1])
            with f_name_c:
                f_name = st.text_input('函数名', key='分段函数的函数名', value='Fibo')
            with f_vars1:
                f_var_1 = st.text_input('参数名1', key='分段函数的变量名1', value='x')
            with f_分段:
                分段数量 = st.number_input('分段数量', value=2, min_value=1, max_value=10, step=1)

            st.markdown(r"""我们只提供最小全功能集的与或非运算和区间与集合的表达方式来表达定义域，特殊符号的输入替代方法见下：

$$
\begin{aligned}  
\begin{aligned}  
\cup &\rightarrow \text{\&} \\
\cap &\rightarrow \text{|} \\
\lnot &\rightarrow \text{\textasciitilde} \\
\mathbb{U} &\rightarrow \text{U} \\
\mathbb{Z} &\rightarrow \text{Z} \\
\mathbb{N} &\rightarrow \text{N} \\
\mathbb{N_0},\mathbb{N^*},\mathbb{N^+},\mathbb{Z^+} &\rightarrow \text{N0 (正整数集合)}
\end{aligned}
\end{aligned}
$$

            """)

            if st.session_state.get('第1段分段函数表达式') is None:
                st.session_state['第1段分段函数表达式'] = "Fibo(x-1) + fibo(x-2)"
                st.session_state['第1段分段函数定义域'] = "N0 & ~{1,2}"
                st.session_state['第2段分段函数表达式'] = "1"
                st.session_state['第2段分段函数定义域'] = "{1,2}"

            for i in range(分段数量):
                表达式, 定义域 = st.columns([7, 3])
                with 表达式:
                    st.session_state[f'第{i + 1}段分段函数表达式'] = st.text_input(f'第{i + 1}段函数表达式', key=f'第{i + 1}段分段函数表达',
                                              value=st.session_state.get(f'第{i + 1}段分段函数表达式'))
                with 定义域:
                    st.session_state[f'第{i + 1}段分段函数定义域'] = domain_exp(
                        st.text_input(f'第{i + 1}段函数定义域', key=f'第{i + 1}段分段函数定义',
                                      value=st.session_state.get(
                                          f'第{i + 1}段分段函数定义域')))

            if st.button('提交', key='分段函数的函数的提交'):
                if f_name in agb.return_all_func().keys():
                    st.error('函数名已存在！')
                else:
                    agb.define_new_func(f_name, var_list=[f_var_1, f_var_2])
                    st.success('函数定义成功！')

        with 俩个参数的可套娃的:
            st.markdown('# 别用，还没写完')
            pass

        # 列出所有已定义的函数
        st.markdown('### 已定义的函数')
        func_dict = agb.return_all_func()
        # 一列列显示所有函数
        show_text = '$$\n' + '\n$$\n$$\n'.join(
            ['{}({})={}'.format(func.replace("_", "\\_"), ", ".join(func_dict[func][1]),
                                sp.latex(func_dict[func][0]))
             for func in func_dict.keys()]) + '\n$$'
        st.markdown(show_text)

with tab2:
    st.markdown('## 绘图')
    if st.session_state.get('submit_button'):

        D2, D3 = st.tabs(['2D绘图', '3D绘图'])
        with D2:
            i_1, i_2 = st.columns(2)
            with i_1:
                x_min = st.number_input('x轴最小值', value=-5, key='2D的x_min')
            with i_2:
                x_max = st.number_input('x轴最大值', value=5, key='2D的x_max')

            if calc_finished:
                s_1, s_2 = st.columns(2)
                with s_1:
                    x = st.selectbox('请选择X轴', agb.return_all_var(), key='2D的x')
                with s_2:
                    gap = st.number_input('绘图间隔', value=0.02, key='2D的gap')

                xx = np.arange(x_min, x_max, gap)
                look_wait_calc = {}
                for var in var_dict:
                    if var != x:
                        look_wait_calc[var] = var_dict[var]
                wait_calc = ans.subs(look_wait_calc)
                st.latex(wait_calc)

                if wait_calc.has(sp.I):
                    st.error('该解析式包含复数i，无法绘图。')
                elif wait_calc.has(sp.oo):
                    st.error('该解析式包含无穷大的量，无法绘图。')
                elif wait_calc.has(sp.zoo):
                    st.error('该解析式包含无穷大的量，且复相未定，无法绘图。')
                elif len(agb.return_all_var()) == 0:
                    st.error('该解析式不含任何变量，无法绘图。')
                    st.stop()
                else:
                    f = sp.lambdify((x), wait_calc, "numpy")
                    Y = f(xx)
                    Y = np.real(Y)
                    fgg = px.line(x=xx, y=Y)
                    fig_html = fgg.to_html()
                    components.html(fig_html, width=1000, height=1000)

        with D3:
            fig = plt.figure()  # 定义新的三维坐标轴
            ax3 = plt.axes(projection='3d')

            i_1, i_2, i_3, i_4 = st.columns([1, 1, 1, 1])
            with i_1:
                x_min = st.number_input('x轴最小值', value=-5, key='3D的x_min')
            with i_2:
                x_max = st.number_input('x轴最大值', value=5, key='3D的x_max')
            with i_3:
                y_min = st.number_input('y轴最小值', value=-5, key='3D的y_min')
            with i_4:
                y_max = st.number_input('y轴最大值', value=5, key='3D的y_max')

            if calc_finished:
                # 定义三维数据

                s_1, s_2, s_3 = st.columns(3)
                # 让用户选择X, Y轴
                select_able = agb.return_all_var().copy()
                if len(select_able) == 0:
                    st.error('该解析式不含任何变量，无法绘图。')
                    st.stop()
                with s_1:
                    x = st.selectbox('请选择X轴', select_able, key='3D的x')
                    select_able.remove(x)
                with s_2:
                    y = st.selectbox('请选择Y轴', select_able, key='3D的y')
                with s_3:
                    gap = st.number_input('绘图间隔', value=0.02, key='3D的gap')

                xx = np.arange(x_min, x_max, gap)
                yy = np.arange(y_min, y_max, gap)
                X, Y = np.meshgrid(xx, yy)

                look_wait_calc = {}
                for var in var_dict:
                    if var != x and var != y:
                        look_wait_calc[var] = var_dict[var]
                wait_calc = ans.subs(look_wait_calc)
                st.latex(wait_calc)
                print('==============')
                print(wait_calc)
                print(agb.return_all_var())
                if wait_calc.has(sp.I):
                    st.error('该解析式包含复数i，无法绘图。')
                elif wait_calc.has(sp.oo):
                    st.error('该解析式包含无穷大的量，无法绘图。')
                elif wait_calc.has(sp.zoo):
                    st.error('该解析式包含无穷大的量，且复相未定，无法绘图。')
                else:
                    f = sp.lambdify((x, y), wait_calc, "numpy")
                    Z = f(X, Y)
                    Z = np.real(Z)

                    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])

                    fig.update_layout(
                        title_text='3D',
                        height=800,
                        width=800,
                        autosize=False,
                        margin=dict(l=65, r=50, b=65, t=90)
                    )

                    fig_html = fig.to_html()
                    components.html(fig_html, height=800, width=800)






