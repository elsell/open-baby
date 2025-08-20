export function dateToLocalTimeString(date: Date): string {
  const time24 = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });

  return time24
}