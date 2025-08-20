function mlToOz(ml: number, precision: number | undefined = undefined): number {
  const val = ml / 29.574

  return precision === undefined ? val : parseFloat(val.toFixed(precision))
}

function ozToMl(oz: number, precision: number | undefined = undefined): number {
  const val = oz * 29.574

  return precision === undefined ? val : parseFloat(val.toFixed(precision))
}

export { mlToOz, ozToMl }