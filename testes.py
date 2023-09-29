import sqlite3
import streamlit as st
import pandas as pd

from datetime import datetime

favicon = "static/imagens/icone1.ico"

st.set_page_config(
    page_title="Auditare - Dashboard",
    page_icon=favicon,
    layout="wide"
)


def create_filtered_df_and_count(df, campo):
    filtered_df = df[df[campo].isin(["Conforme", "Não Conforme", "Não se Aplica"])]
    filtered_df['Contagem'] = 1
    grouped_df = filtered_df.groupby(campo)['Contagem'].count().reset_index()
    return grouped_df


def main():
    caminho_db = '//10.0.0.70/Bando de Dados Integra/Integrasistema.db'

    nomes_formularios = {
        "formulario1": "Ambulatoriais em Especialidades",
        "formulario2": "Diagnóstica em Radiologia",
        "formulario3": "Diagnóstica em Endoscopia",
        "formulario4": "Procedimentos Cirúrgicos"
    }

    st.title("Análise de Dados dos Formulários")

    tabela_selecionada = st.sidebar.selectbox("Selecione o formulário para análise", list(nomes_formularios.values()))

    tabela_para_nome = {v: k for k, v in nomes_formularios.items()}
    nome_tabela = tabela_para_nome.get(tabela_selecionada, None)

    if nome_tabela:
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {nome_tabela}")
        dados = cursor.fetchall()
        conn.close()
        col_names = [i[0] for i in cursor.description]
        df = pd.DataFrame(dados, columns=col_names)
        df['Data'] = pd.to_datetime(df['Data'])
        campos_validos = [col for col in col_names if
                          col not in ['id', 'Nome', 'Prontuario', 'Atendimento', 'ambulatorio_selecionado',
                                      'caixaDeTexto', 'Status', 'Usuario', 'Data']]

        status_colors = {
            "Conforme": "green",
            "Não Conforme": "red",
            "Não se Aplica": "blue"
        }

        st.subheader(f"Comparação de Status - {tabela_selecionada}")

        # Dividir a tela em duas colunas
        col1, col2 = st.columns(2)

        with col1:
            fig_status = px.bar(df, x="Status", title=f"Comparação de Status - {tabela_selecionada}",
                                color="Status",
                                color_discrete_map=status_colors,
                                category_orders={"Status": ["Conforme", "Não Conforme", "Não se Aplica"]})

            for i in range(len(fig_status.data)):
                status = fig_status.data[i]['x'][0]
                count = df[df['Status'] == status].shape[0]
                fig_status.add_trace(
                    go.Scatter(
                        x=[status],
                        y=[count],
                        text=[count],
                        mode="text",
                        textposition="top center",
                        showlegend=False
                    )
                )

            st.plotly_chart(fig_status, use_container_width=True)

        with col2:
            status_counts = df['Status'].value_counts()
            total_prontuarios = len(df)
            status_percentages = (status_counts / total_prontuarios) * 100
            fig_pizza = px.pie(status_percentages, values=status_percentages, names=status_percentages.index,
                               title="Porcentagem de Status em relação ao total de prontuários auditados")
            st.plotly_chart(fig_pizza, use_container_width=True)

        total_prontuarios = df.shape[0]
        st.sidebar.subheader("Quantidade Total de Prontuários Auditados")
        st.sidebar.info(total_prontuarios)

        nomes_auditores = df['Usuario'].unique()
        st.sidebar.subheader("Auditores")
        st.sidebar.info(", ".join(nomes_auditores))

        periodo_avaliacao = df['Data'].min().strftime('%d/%m/%Y') + " - " + df['Data'].max().strftime('%d/%m/%Y')
        st.sidebar.subheader("Período da Avaliação")
        st.sidebar.info(periodo_avaliacao)

        campo_selecionado = st.sidebar.selectbox("Selecione um campo para análise", campos_validos)

        grouped_df = create_filtered_df_and_count(df, campo_selecionado)

        fig = px.bar(grouped_df, x=campo_selecionado, y='Contagem',
                     title=f"Comparação para o Campo: {campo_selecionado}",
                     color=campo_selecionado, color_discrete_map=status_colors, text='Contagem')

        st.plotly_chart(fig, use_container_width=True)
    # Criar um campo para selecionar o usuário
        selected_user = st.sidebar.selectbox("Selecione um Usuário", df['Usuario'].unique())

        # Filtrar o DataFrame com base no usuário selecionado
        filtered_df = df[df['Usuario'] == selected_user]

        # Exibir a tabela com as marcações do usuário selecionado
        st.subheader(f"Marcações por Usuário: {selected_user}")
        st.write(filtered_df)

if __name__ == "__main__":
    main()
