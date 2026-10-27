import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(cleanup)

if (typeof HTMLDialogElement.prototype.showModal !== 'function') {
  const fecharComEsc = function (this: HTMLDialogElement, evento: KeyboardEvent) {
    if (evento.key !== 'Escape') return
    if (this.dispatchEvent(new Event('cancel', { cancelable: true }))) this.close()
  }

  HTMLDialogElement.prototype.showModal = function (this: HTMLDialogElement) {
    this.setAttribute('open', '')
    this.addEventListener('keydown', fecharComEsc)
  }

  HTMLDialogElement.prototype.close = function (this: HTMLDialogElement) {
    if (!this.open) return
    this.removeAttribute('open')
    this.removeEventListener('keydown', fecharComEsc)
    this.dispatchEvent(new Event('close'))
  }
}
