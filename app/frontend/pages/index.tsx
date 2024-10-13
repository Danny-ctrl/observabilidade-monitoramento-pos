import React, { useState } from "react"; // Importa React e o hook useState
import styles from "../styles/Home.module.css"; // Importa os estilos CSS
import { apm } from "@elastic/apm-rum"; // Importa o cliente APM do Elastic para monitoramento

export default function Home() {
  // Estados para armazenar os alunos e o nome do aluno a ser cadastrado
  const [alunos, setAlunos] = useState([]);
  const [values, setValues] = useState({ nome: "" });

  // Função para listar os alunos cadastrados
  async function listarAlunos() {
    try {
      // Faz uma requisição GET para listar os alunos
      const response = await fetch("http://localhost:9000/listar_alunos");
      const data = await response.json();
      setAlunos(data); // Atualiza o estado com os alunos recebidos
    } catch (err) {
      alert("Requisição não foi realizada"); // Mostra um alerta em caso de erro
    }
  }

  // Função para simular e receber um erro 500 do backend
  async function receberErro() {
    try {
      // Faz uma requisição GET para a rota que gera o erro
      const response = await fetch("http://localhost:9000/receber_erro");
      if (!response.ok) {
        // Caso a resposta não seja OK, lança um erro
        throw new Error(`Erro HTTP: ${response.status} ${response.statusText}`);
      }
      const data = await response.json();
      console.log(data); // Mostra o resultado no console
    } catch (err) {
      alert("Requisição não foi realizada: " + err.message); // Mostra um alerta em caso de erro
    }
  }

  // Função para cadastrar um novo aluno
  async function cadastrarAluno(e) {
    e.preventDefault(); // Evita o comportamento padrão do form de recarregar a página
    try {
      // Faz uma requisição POST para cadastrar o aluno
      const response = await fetch("http://localhost:9000/cadastrar_aluno", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Define o tipo de conteúdo como JSON
        },
        body: JSON.stringify(values), // Envia os dados do aluno no corpo da requisição
      });
      if (!response.ok) {
        throw new Error("Erro na requisição: " + response.statusText);
      }
      const data = await response.json();
      alert(data); // Mostra uma mensagem com a resposta do servidor
      await listarAlunos(); // Atualiza a lista de alunos após o cadastro
      setValues({ nome: "" }); // Reseta o valor do input
    } catch (err) {
      alert("Requisição não foi realizada: " + err.message); // Mostra um alerta em caso de erro
    }
  }

  // Função para alternar o status online/offline do aluno
  async function acessarSistema(alunoId) {
    try {
      // Faz uma requisição POST para atualizar o status do aluno
      const response = await fetch(
        `http://localhost:9000/acessar_sistema/${alunoId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json", // Define o tipo de conteúdo como JSON
          },
        }
      );
      if (!response.ok) {
        throw new Error("Erro na requisição: " + response.statusText);
      }
      const data = await response.json();
      console.log("Status do aluno atualizado:", data); // Exibe a resposta no console
      await listarAlunos(); // Atualiza a lista de alunos após a alteração
    } catch (err) {
      alert("Requisição não foi realizada: " + err.message); // Mostra um alerta em caso de erro
    }
  }

  // JSX que renderiza a interface da página
  return (
    <main className={styles.main}>
      <h1 className={styles.title}>
        MBA em Engenharia de Software | MBA USP/Esalq
      </h1>
      {/* Formulário para cadastrar um aluno */}
      <form onSubmit={cadastrarAluno} className={styles.form}>
        <input
          type="text"
          placeholder="Nome do aluno"
          value={values.nome} // Valor do input controlado pelo estado
          onChange={(e) => setValues({ ...values, nome: e.target.value })} // Atualiza o estado ao digitar
          className={styles.input}
        />
        <button className={styles.button} type="submit"  name="cadastrar-aluno">
          Cadastrar aluno
        </button>
      </form>

      {/* Botão para listar os alunos */}
      <button className={styles.listButton} name="listar-alunos" onClick={listarAlunos}>
        Listar alunos
      </button>

      {/* Tabela que exibe a lista de alunos e seu status */}
      <table className={styles.table}>
        <thead>
          <tr>
            <th className={styles.tableHead}>Aluno</th>
            <th className={styles.tableHead}>Status</th>
          </tr>
        </thead>
        <tbody>
          {alunos.map((aluno, index) => (
            <tr key={index}>
              <td className={styles.tableCell}>{aluno.nome}</td>
              <td className={styles.tableCell}>
                {/* Botão que alterna o status do aluno entre online e offline */}
                <button
                  name="acessar-sistema"
                  onClick={() => acessarSistema(aluno.id)}
                  className={
                    aluno.online ? styles.onlineButton : styles.offlineButton
                  }
                >
                  {aluno.online ? "Online" : "Offline"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Botão para simular um erro 500 */}
      <button className={styles.errorButton} name="simular-erro" onClick={receberErro}>
        Botão erro 500
      </button>
    </main>
  );
}
