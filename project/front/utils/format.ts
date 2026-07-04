/**
 * 숫자를 한국 원화 형식(예: 15,000원)으로 포맷팅합니다.
 * @param value 포맷팅할 숫자
 * @returns 포맷팅된 문자열
 */
export const formatPrice = (value: number) => {
  if (value === undefined || value === null) return '0원'
  return value.toLocaleString() + '원'
}
