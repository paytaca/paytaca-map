import { describe, it, expect } from 'vitest'

import { formatMerchantLocation } from '../location'

describe('formatMerchantLocation', () => {
  it('uses city and country when a city is present', () => {
    expect(formatMerchantLocation({ city: 'Tacloban', country: 'Philippines' })).toBe(
      'Tacloban, Philippines',
    )
  })

  it('uses town, province and country when only a town is present', () => {
    expect(
      formatMerchantLocation({ town: 'Palo', province: 'Leyte', country: 'Philippines' }),
    ).toBe('Palo, Leyte, Philippines')
  })

  it('falls back to state and country when there is no city or town', () => {
    expect(formatMerchantLocation({ state: 'California', country: 'United States' })).toBe(
      'California, United States',
    )
  })

  it('falls back to province when state is missing', () => {
    expect(formatMerchantLocation({ province: 'Leyte', country: 'Philippines' })).toBe(
      'Leyte, Philippines',
    )
  })

  it('renders only the country when no other location parts are known', () => {
    expect(formatMerchantLocation({ country: 'Philippines' })).toBe('Philippines')
  })

  it('trims values and ignores blank fields', () => {
    expect(formatMerchantLocation({ city: '  ', state: ' Texas ', country: 'USA' })).toBe(
      'Texas, USA',
    )
  })

  it('avoids repeating identical parts', () => {
    expect(formatMerchantLocation({ city: 'Singapore', country: 'Singapore' })).toBe('Singapore')
  })

  it('returns an empty string for missing merchants', () => {
    expect(formatMerchantLocation(null)).toBe('')
    expect(formatMerchantLocation(undefined)).toBe('')
  })
})
