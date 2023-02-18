import streamlit as st

st.title('Sobre o projeto')

st.write('Projeto desenvolvido com o objetivo de criar um dashboard interativo para apresentação de dados da disciplina de Visualização de Dados da CESAR School.')
st.write('''O dashboard foi desenvolvido utilizando tecnologias de visualização de dados para apresentar de forma clara e intuitiva informações relevantes para a disciplina.
 São exibidos gráficos e tabelas dinâmicas para facilitar a compreensão dos dados, além de painéis interativos para que os usuários possam explorar os dados de maneira mais aprofundada,
 tendo sido realizada a prepararação dos dados para serem apresentados no dashboard, considerando aspectos como limpeza, integração e normalização dos dados.
 O dashboard foi desenvolvido utilizando ferramentas de visualização de dados como Streamlit e Plotly. ''')

st.markdown('''
Algumas das funcionalidades previstas para o dashboard incluem:

- Opção de upload de dataset para análise;
- Exibição de gráficos dinâmicos para visualização de tendências e comparações;
- Filtros interativos para seleção de informações relevantes;
- Painéis com informações detalhadas sobre os dados selecionados;
''')

st.write('Github: https://github.com/EdmilsonSantana/recalls-dashboard')

# Github
st.subheader('Equipe')
st.write('O projeto foi desenvolvido por uma equipe de estudantes da disciplina de Visualização de Dados, com supervisão do professor Eronides da CESAR School.')
st.markdown('''
- Edmilson Manoel Guilherme de Santana (emgs@cesar.school)
- Lucas Cristiano Calixto Dantas (lccd@cesar.school)
''')

# definições do dataset
