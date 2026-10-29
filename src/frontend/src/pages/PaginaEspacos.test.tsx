import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes, useLocation } from 'react-router'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ErroDaApi } from '../api/cliente.ts'
import {
  ativarEspaco,
  cadastrarEspaco,
  desativarEspaco,
  editarEspaco,
  listarEspacos,
  listarTiposDeEspaco,
  type Espaco,
} from '../api/espacos.ts'
import type { RespostaSucesso } from '../api/tipos.ts'
import { renderizarComProvedores, valorDaSessao } from '../testes/renderizar.tsx'
import { USUARIO_GESTOR, USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import PaginaEspacos from './PaginaEspacos.tsx'

vi.mock('../api/espacos.ts', () => ({
  listarEspacos: vi.fn(),
  listarTiposDeEspaco: vi.fn(),
  cadastrarEspaco: vi.fn(),
  editarEspaco: vi.fn(),
  desativarEspaco: vi.fn(),
  ativarEspaco: vi.fn(),
}))

const TIPOS = [
  { valor: 'QUADRA_POLIESPORTIVA', rotulo: 'Quadra poliesportiva' },
  { valor: 'GINASIO', rotulo: 'Ginásio' },
]

const GINASIO: Espaco = {
  id: 1,
  nome: 'Ginásio A',
  tipo: 'GINASIO',
  tipo_rotulo: 'Ginásio',
  capacidade: 50,
  ativo: true,
}

const QUADRA: Espaco = {
  id: 2,
  nome: 'Quadra Antiga',
  tipo: 'QUADRA_POLIESPORTIVA',
  tipo_rotulo: 'Quadra poliesportiva',
  capacidade: 20,
  ativo: false,
}

function lista(dados: Espaco[], mensagem: string): RespostaSucesso<Espaco[]> {
  return { mensagem, dados }
}

function promessaControlada<T>() {
  let resolver!: (valor: T) => void
  const promessa = new Promise<T>((resolve) => {
    resolver = resolve
  })
  return { promessa, resolver }
}

function BuscaAtual() {
  return <output data-testid="busca">{useLocation().search}</output>
}

function renderizar(caminho = '/espacos', usuario = USUARIO_GESTOR) {
  renderizarComProvedores(
    <Routes>
      <Route
        path="/espacos"
        element={
          <>
            <PaginaEspacos />
            <BuscaAtual />
          </>
        }
      />
    </Routes>,
    { caminho, sessao: valorDaSessao({ usuario }) },
  )
}

function secaoDoCadastro() {
  return within(screen.getByRole('region', { name: 'Cadastrar espaço' }))
}

function secaoDaLista() {
  return within(screen.getByRole('region', { name: 'Espaços cadastrados' }))
}

async function preencherFormulario(dados: { nome?: string; tipo?: string; capacidade?: string }) {
  const formulario = secaoDoCadastro()
  await formulario.findByLabelText('Nome')
  if (dados.nome) await userEvent.type(formulario.getByLabelText('Nome'), dados.nome)
  if (dados.tipo) await userEvent.selectOptions(formulario.getByLabelText('Tipo'), dados.tipo)
  if (dados.capacidade) {
    await userEvent.type(formulario.getByLabelText('Capacidade'), dados.capacidade)
  }
}

async function enviarFormulario() {
  await userEvent.click(secaoDoCadastro().getByRole('button', { name: 'Cadastrar espaço' }))
}

function valorDe(rotulo: string) {
  return (secaoDoCadastro().getByLabelText(rotulo) as HTMLInputElement | HTMLSelectElement).value
}

function espacoAtualizado(espaco: Espaco): RespostaSucesso<Espaco> {
  return { mensagem: 'Espaço atualizado com sucesso.', dados: espaco }
}

async function abrirDialogo(nomeDoBotao: string, tituloDoDialogo: string) {
  await userEvent.click(await secaoDaLista().findByRole('button', { name: nomeDoBotao }))
  return within(screen.getByRole('dialog', { name: tituloDoDialogo }))
}

function valorNoDialogo(dialogo: ReturnType<typeof within>, rotulo: string) {
  return (dialogo.getByLabelText(rotulo) as HTMLInputElement | HTMLSelectElement).value
}

describe('PaginaEspacos', () => {
  beforeEach(() => {
    vi.mocked(listarEspacos).mockReset()
    vi.mocked(listarTiposDeEspaco).mockReset()
    vi.mocked(cadastrarEspaco).mockReset()
    vi.mocked(editarEspaco).mockReset()
    vi.mocked(desativarEspaco).mockReset()
    vi.mocked(ativarEspaco).mockReset()
    vi.mocked(listarTiposDeEspaco).mockResolvedValue({
      mensagem: 'Tipos de espaço disponíveis.',
      dados: TIPOS,
    })
    vi.mocked(listarEspacos).mockResolvedValue(
      lista([GINASIO, QUADRA], '2 espaços encontrados.'),
    )
  })

  it('mostra a mensagem de contagem e os espaços na tabela', async () => {
    renderizar()

    const tabela = await secaoDaLista().findByRole('table', { name: '2 espaços encontrados.' })
    const linhas = within(tabela).getAllByRole('row')
    expect(linhas).toHaveLength(3)
    expect(within(linhas[1]).getByRole('rowheader').textContent).toBe('Ginásio A')
    expect(linhas[1].textContent).toContain('Ativo')
    expect(linhas[2].textContent).toContain('Quadra poliesportiva')
    expect(linhas[2].textContent).toContain('Inativo')
    expect(listarEspacos).toHaveBeenCalledWith({ tipo: '', apenasAtivos: false })
  })

  it('sem filtros e sem espaços, convida a cadastrar o primeiro', async () => {
    vi.mocked(listarEspacos).mockResolvedValue(lista([], 'Nenhum espaço encontrado.'))

    renderizar()

    expect(await secaoDaLista().findByText('Nenhum espaço cadastrado')).toBeTruthy()
    expect(secaoDaLista().getByText('Use o formulário acima para cadastrar o primeiro.')).toBeTruthy()
    expect(secaoDaLista().queryByRole('button', { name: 'Limpar filtros' })).toBeNull()
  })

  it('lê os filtros da URL e, sem resultado, "Limpar filtros" limpa a URL e busca de novo', async () => {
    vi.mocked(listarEspacos).mockResolvedValueOnce(lista([], 'Nenhum espaço encontrado.'))
    renderizar('/espacos?tipo=GINASIO&apenas_ativos=true')

    expect(await secaoDaLista().findByText('Nenhum espaço encontrado')).toBeTruthy()
    expect(listarEspacos).toHaveBeenLastCalledWith({ tipo: 'GINASIO', apenasAtivos: true })
    expect((secaoDaLista().getByLabelText('Somente ativos') as HTMLInputElement).checked).toBe(true)

    await userEvent.click(secaoDaLista().getByRole('button', { name: 'Limpar filtros' }))

    expect(screen.getByTestId('busca').textContent).toBe('')
    expect(await secaoDaLista().findByRole('table')).toBeTruthy()
    expect(listarEspacos).toHaveBeenLastCalledWith({ tipo: '', apenasAtivos: false })
  })

  it('mudar os filtros grava na URL e busca com eles', async () => {
    renderizar()
    const filtroDeTipo = secaoDaLista().getByLabelText('Tipo')
    await waitFor(() => expect((filtroDeTipo as HTMLSelectElement).disabled).toBe(false))

    await userEvent.selectOptions(filtroDeTipo, 'GINASIO')

    expect(listarEspacos).toHaveBeenLastCalledWith({ tipo: 'GINASIO', apenasAtivos: false })
    expect(screen.getByTestId('busca').textContent).toBe('?tipo=GINASIO')

    await userEvent.click(secaoDaLista().getByLabelText('Somente ativos'))

    expect(listarEspacos).toHaveBeenLastCalledWith({ tipo: 'GINASIO', apenasAtivos: true })
    expect(screen.getByTestId('busca').textContent).toBe('?tipo=GINASIO&apenas_ativos=true')
  })

  it('cadastro com sucesso mostra o toast, limpa o formulário e recarrega a lista', async () => {
    vi.mocked(cadastrarEspaco).mockResolvedValue({
      mensagem: 'Espaço cadastrado com sucesso.',
      dados: GINASIO,
    })
    renderizar()
    await secaoDaLista().findByRole('table')
    await preencherFormulario({ nome: 'Ginásio A', tipo: 'GINASIO', capacidade: '50' })

    await enviarFormulario()

    expect(await screen.findByText('Espaço cadastrado com sucesso.')).toBeTruthy()
    expect(cadastrarEspaco).toHaveBeenCalledWith({
      nome: 'Ginásio A',
      tipo: 'GINASIO',
      capacidade: '50',
    })
    expect(valorDe('Nome')).toBe('')
    expect(valorDe('Tipo')).toBe('')
    expect(valorDe('Capacidade')).toBe('')
    await waitFor(() => expect(listarEspacos).toHaveBeenCalledTimes(2))
  })

  it('erro de campo aparece embaixo do campo, recebe o foco e some ao editar', async () => {
    vi.mocked(cadastrarEspaco).mockRejectedValue(
      new ErroDaApi(400, 'CAPACIDADE_INVALIDA', 'A capacidade deve ser um número inteiro maior que zero.', {
        capacidade: ['A capacidade deve ser um número inteiro maior que zero.'],
      }),
    )
    renderizar()
    await preencherFormulario({ nome: 'Ginásio A', tipo: 'GINASIO', capacidade: '0' })

    await enviarFormulario()

    const capacidade = secaoDoCadastro().getByLabelText('Capacidade')
    await waitFor(() => expect(document.activeElement).toBe(capacidade))
    expect(capacidade.getAttribute('aria-invalid')).toBe('true')
    expect(
      secaoDoCadastro().getByText('A capacidade deve ser um número inteiro maior que zero.'),
    ).toBeTruthy()
    expect(secaoDoCadastro().queryByRole('alert')).toBeNull()

    await userEvent.type(capacidade, '5')

    expect(capacidade.getAttribute('aria-invalid')).toBeNull()
    expect(secaoDoCadastro().queryByText('A capacidade deve ser um número inteiro maior que zero.')).toBeNull()
  })

  it('nome repetido aparece no campo Nome', async () => {
    vi.mocked(cadastrarEspaco).mockRejectedValue(
      new ErroDaApi(409, 'NOME_DE_ESPACO_JA_CADASTRADO', 'Já existe um espaço com este nome.', {
        nome: ['Já existe um espaço com este nome.'],
      }),
    )
    renderizar()
    await preencherFormulario({ nome: 'Ginásio A', tipo: 'GINASIO', capacidade: '10' })

    await enviarFormulario()

    const nome = secaoDoCadastro().getByLabelText('Nome')
    await waitFor(() => expect(document.activeElement).toBe(nome))
    expect(secaoDoCadastro().getByText('Já existe um espaço com este nome.')).toBeTruthy()
  })

  it('erro sem campos aparece num aviso no topo do formulário', async () => {
    vi.mocked(cadastrarEspaco).mockRejectedValue(
      new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'),
    )
    renderizar()
    await preencherFormulario({ nome: 'Ginásio A' })

    await enviarFormulario()

    const aviso = await secaoDoCadastro().findByRole('alert')
    expect(aviso.textContent).toContain('Não foi possível conectar ao servidor.')
    expect(valorDe('Nome')).toBe('Ginásio A')
  })

  it('desabilita o botão enquanto envia', async () => {
    const pendente = promessaControlada<RespostaSucesso<Espaco>>()
    vi.mocked(cadastrarEspaco).mockReturnValue(pendente.promessa)
    renderizar()
    await preencherFormulario({ nome: 'Ginásio A', tipo: 'GINASIO', capacidade: '50' })

    await enviarFormulario()

    const botao = secaoDoCadastro().getByRole('button', { name: 'Cadastrando...' })
    expect((botao as HTMLButtonElement).disabled).toBe(true)

    pendente.resolver({ mensagem: 'Espaço cadastrado com sucesso.', dados: GINASIO })

    const liberado = await secaoDoCadastro().findByRole('button', { name: 'Cadastrar espaço' })
    expect((liberado as HTMLButtonElement).disabled).toBe(false)
  })

  it('mostra um erro com "Tentar novamente" quando os tipos não carregam', async () => {
    vi.mocked(listarTiposDeEspaco)
      .mockRejectedValueOnce(new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'))
      .mockResolvedValueOnce({ mensagem: 'Tipos de espaço disponíveis.', dados: TIPOS })
    renderizar()

    await userEvent.click(
      await secaoDoCadastro().findByRole('button', { name: 'Tentar novamente' }),
    )

    expect(await secaoDoCadastro().findByLabelText('Nome')).toBeTruthy()
  })

  it('para o solicitante, troca o formulário por um aviso e lista os espaços', async () => {
    vi.mocked(listarEspacos).mockResolvedValue(lista([], 'Nenhum espaço encontrado.'))

    renderizar('/espacos', USUARIO_SOLICITANTE)

    expect(screen.getByText('Somente o gestor cadastra espaços.')).toBeTruthy()
    expect(screen.queryByRole('region', { name: 'Cadastrar espaço' })).toBeNull()
    expect(screen.queryByRole('button', { name: 'Cadastrar espaço' })).toBeNull()
    expect(await secaoDaLista().findByText('Nenhum espaço cadastrado')).toBeTruthy()
    expect(secaoDaLista().queryByText('Use o formulário acima para cadastrar o primeiro.')).toBeNull()
  })

  it('para o solicitante, a tabela não tem editar, desativar nem reativar', async () => {
    renderizar('/espacos', USUARIO_SOLICITANTE)

    await secaoDaLista().findByRole('table')

    expect(secaoDaLista().queryByRole('button', { name: /Editar|Desativar|Reativar/ })).toBeNull()
    expect(secaoDaLista().getByRole('link', { name: 'Reservar Ginásio A' })).toBeTruthy()
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  describe('edição', () => {
    it('abre o diálogo com os dados do espaço', async () => {
      renderizar()

      const dialogo = await abrirDialogo('Editar o espaço Ginásio A', 'Editar espaço')

      expect(valorNoDialogo(dialogo, 'Nome')).toBe('Ginásio A')
      expect(valorNoDialogo(dialogo, 'Tipo')).toBe('GINASIO')
      expect(valorNoDialogo(dialogo, 'Capacidade')).toBe('50')
      expect(document.activeElement).toBe(dialogo.getByLabelText('Nome'))
    })

    it('envia só o campo alterado; no sucesso, mostra o toast, fecha e recarrega a lista', async () => {
      vi.mocked(editarEspaco).mockResolvedValue(espacoAtualizado({ ...GINASIO, capacidade: 60 }))
      renderizar()
      const dialogo = await abrirDialogo('Editar o espaço Ginásio A', 'Editar espaço')

      await userEvent.clear(dialogo.getByLabelText('Capacidade'))
      await userEvent.type(dialogo.getByLabelText('Capacidade'), '60')
      await userEvent.click(dialogo.getByRole('button', { name: 'Salvar alterações' }))

      expect(editarEspaco).toHaveBeenCalledWith(1, { capacidade: '60' })
      expect(await screen.findByText('Espaço atualizado com sucesso.')).toBeTruthy()
      expect(screen.queryByRole('dialog')).toBeNull()
      await waitFor(() => expect(listarEspacos).toHaveBeenCalledTimes(2))
      const regiao = await secaoDaLista().findByRole('region', { name: '2 espaços encontrados.' })
      await waitFor(() => expect(document.activeElement).toBe(regiao))
    })

    it('a capacidade inválida aparece embaixo do campo, que recebe o foco', async () => {
      const mensagem = 'A capacidade deve ser um número inteiro maior que zero.'
      vi.mocked(editarEspaco).mockRejectedValue(
        new ErroDaApi(400, 'CAPACIDADE_INVALIDA', mensagem, { capacidade: [mensagem] }),
      )
      renderizar()
      const dialogo = await abrirDialogo('Editar o espaço Ginásio A', 'Editar espaço')

      await userEvent.clear(dialogo.getByLabelText('Capacidade'))
      await userEvent.type(dialogo.getByLabelText('Capacidade'), '0')
      await userEvent.click(dialogo.getByRole('button', { name: 'Salvar alterações' }))

      const capacidade = dialogo.getByLabelText('Capacidade')
      await waitFor(() => expect(document.activeElement).toBe(capacidade))
      expect(capacidade.getAttribute('aria-invalid')).toBe('true')
      expect(dialogo.getByText(mensagem)).toBeTruthy()
      expect(dialogo.queryByRole('alert')).toBeNull()
    })

    it('o nome repetido aparece no campo Nome', async () => {
      const mensagem = 'Já existe um espaço com este nome.'
      vi.mocked(editarEspaco).mockRejectedValue(
        new ErroDaApi(409, 'NOME_DE_ESPACO_JA_CADASTRADO', mensagem, { nome: [mensagem] }),
      )
      renderizar()
      const dialogo = await abrirDialogo('Editar o espaço Ginásio A', 'Editar espaço')

      await userEvent.clear(dialogo.getByLabelText('Nome'))
      await userEvent.type(dialogo.getByLabelText('Nome'), 'Quadra Antiga')
      await userEvent.click(dialogo.getByRole('button', { name: 'Salvar alterações' }))

      expect(editarEspaco).toHaveBeenCalledWith(1, { nome: 'Quadra Antiga' })
      const nome = dialogo.getByLabelText('Nome')
      await waitFor(() => expect(document.activeElement).toBe(nome))
      expect(dialogo.getByText(mensagem)).toBeTruthy()
    })

    it('sem mudança, envia um corpo vazio e mostra a mensagem da API num aviso', async () => {
      vi.mocked(editarEspaco).mockRejectedValue(
        new ErroDaApi(400, 'NENHUMA_ALTERACAO_INFORMADA', 'Informe ao menos um campo para alterar.'),
      )
      renderizar()
      const dialogo = await abrirDialogo('Editar o espaço Ginásio A', 'Editar espaço')

      await userEvent.click(dialogo.getByRole('button', { name: 'Salvar alterações' }))

      expect(editarEspaco).toHaveBeenCalledWith(1, {})
      const aviso = await dialogo.findByRole('alert')
      expect(aviso.textContent).toContain('Informe ao menos um campo para alterar.')
      expect(screen.getByRole('dialog', { name: 'Editar espaço' })).toBeTruthy()
    })
  })

  describe('desativação e reativação', () => {
    it('o diálogo explica que as reservas existentes continuam valendo', async () => {
      renderizar()

      const dialogo = await abrirDialogo('Desativar o espaço Ginásio A', 'Desativar espaço')

      expect(
        dialogo.getByText(
          'Novas reservas ficarão bloqueadas. As reservas já existentes continuam valendo; ' +
            'cancele-as na tela de reservas, se precisar.',
        ),
      ).toBeTruthy()
      expect(document.activeElement).toBe(dialogo.getByRole('button', { name: 'Voltar' }))
    })

    it('desativar com sucesso mostra o toast, fecha e recarrega a lista', async () => {
      const mensagem =
        'Espaço desativado. Novas reservas ficam bloqueadas; as existentes continuam valendo.'
      vi.mocked(desativarEspaco).mockResolvedValue({
        mensagem,
        dados: { ...GINASIO, ativo: false },
      })
      renderizar()
      const dialogo = await abrirDialogo('Desativar o espaço Ginásio A', 'Desativar espaço')

      await userEvent.click(dialogo.getByRole('button', { name: 'Desativar espaço' }))

      expect(desativarEspaco).toHaveBeenCalledWith(1)
      expect(await screen.findByText(mensagem)).toBeTruthy()
      expect(screen.queryByRole('dialog')).toBeNull()
      await waitFor(() => expect(listarEspacos).toHaveBeenCalledTimes(2))
    })

    it('com 409, mostra o aviso e "Atualizar lista", que fecha e recarrega', async () => {
      vi.mocked(desativarEspaco).mockRejectedValue(
        new ErroDaApi(409, 'ESPACO_JA_INATIVO', 'Este espaço já está inativo.'),
      )
      renderizar()
      const dialogo = await abrirDialogo('Desativar o espaço Ginásio A', 'Desativar espaço')

      await userEvent.click(dialogo.getByRole('button', { name: 'Desativar espaço' }))

      const aviso = await dialogo.findByRole('alert')
      expect(aviso.textContent).toContain('Este espaço já está inativo.')
      await userEvent.click(dialogo.getByRole('button', { name: 'Atualizar lista' }))

      expect(screen.queryByRole('dialog')).toBeNull()
      await waitFor(() => expect(listarEspacos).toHaveBeenCalledTimes(2))
    })

    it('reativar chama a API de ativar para o espaço inativo', async () => {
      vi.mocked(ativarEspaco).mockResolvedValue({
        mensagem: 'Espaço reativado.',
        dados: { ...QUADRA, ativo: true },
      })
      renderizar()
      const dialogo = await abrirDialogo('Reativar o espaço Quadra Antiga', 'Reativar espaço')

      expect(dialogo.getByText('O espaço voltará a aceitar novas reservas.')).toBeTruthy()
      await userEvent.click(dialogo.getByRole('button', { name: 'Reativar espaço' }))

      expect(ativarEspaco).toHaveBeenCalledWith(2)
      expect(desativarEspaco).not.toHaveBeenCalled()
      expect(await screen.findByText('Espaço reativado.')).toBeTruthy()
    })

    it('"Voltar" fecha sem chamar a API e devolve o foco ao botão da linha', async () => {
      renderizar()
      const botao = await secaoDaLista().findByRole('button', {
        name: 'Desativar o espaço Ginásio A',
      })
      await userEvent.click(botao)

      await userEvent.click(
        within(screen.getByRole('dialog', { name: 'Desativar espaço' })).getByRole('button', {
          name: 'Voltar',
        }),
      )

      expect(screen.queryByRole('dialog')).toBeNull()
      expect(desativarEspaco).not.toHaveBeenCalled()
      expect(document.activeElement).toBe(botao)
    })
  })
})
