import type { DadosDoEspaco, TipoDeEspaco } from '../../api/espacos.ts'
import Campo from '../formulario/Campo.tsx'

type PropriedadesDosCampos = {
  dados: DadosDoEspaco
  tipos: TipoDeEspaco[]
  errosDosCampos: Record<string, string>
  aoAlterar: (campo: keyof DadosDoEspaco, valor: string) => void
}

function CamposDoEspaco({ dados, tipos, errosDosCampos, aoAlterar }: PropriedadesDosCampos) {
  return (
    <>
      <Campo rotulo="Nome" erro={errosDosCampos.nome}>
        {(controle) => (
          <input
            {...controle}
            type="text"
            name="nome"
            autoComplete="off"
            value={dados.nome}
            onChange={(evento) => aoAlterar('nome', evento.target.value)}
          />
        )}
      </Campo>
      <Campo rotulo="Tipo" erro={errosDosCampos.tipo}>
        {(controle) => (
          <select
            {...controle}
            name="tipo"
            value={dados.tipo}
            onChange={(evento) => aoAlterar('tipo', evento.target.value)}
          >
            <option value="">Selecione o tipo</option>
            {tipos.map(({ valor, rotulo }) => (
              <option key={valor} value={valor}>
                {rotulo}
              </option>
            ))}
          </select>
        )}
      </Campo>
      <Campo
        rotulo="Capacidade"
        dica="Número máximo de pessoas."
        erro={errosDosCampos.capacidade}
      >
        {(controle) => (
          <input
            {...controle}
            type="number"
            inputMode="numeric"
            name="capacidade"
            value={dados.capacidade}
            onChange={(evento) => aoAlterar('capacidade', evento.target.value)}
          />
        )}
      </Campo>
    </>
  )
}

export default CamposDoEspaco
