const clean = (value) => (typeof value === 'string' ? value.trim() : '');

const joinParts = (parts) => {
  const seen = new Set();

  return parts
    .filter((part) => {
      if (!part) return false;

      const key = part.toLowerCase();
      if (seen.has(key)) return false;

      seen.add(key);
      return true;
    })
    .join(', ');
};

/**
 * Format a merchant's location for display.
 *
 * Falls back progressively when parts are missing, e.g. when a merchant has no
 * city or town the address is rendered as "{state}, {country}".
 */
export function formatMerchantLocation(merchant) {
  if (!merchant) return '';

  const city = clean(merchant.city);
  const town = clean(merchant.town);
  const region = clean(merchant.province) || clean(merchant.state);
  const country = clean(merchant.country);

  if (city) return joinParts([city, country]);
  if (town) return joinParts([town, region, country]);

  return joinParts([region, country]);
}
