declare const process: { env: Record<string, string | undefined> }

export function setup() {
  process.env.TZ = 'America/Sao_Paulo'
}
