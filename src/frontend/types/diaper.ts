enum DiaperType {
    PEE = "pee",
    POOP = "poop",
    BOTH = "both"
}

enum DiaperColor {
    YELLOW = "yellow",
    BROWN = "brown",
    GREEN = "green",
    BLACK = "black"
}

enum DiaperConsistency {
    WATERY = "watery",
    PASTY = "pasty"
}

enum DiaperSize {
    SMALL = "small",
    MEDIUM = "medium",
    LARGE = "large"
}

function toDiaperType(value: string): DiaperType {
    if (Object.values(DiaperType).includes(value as DiaperType)) {
        return value as DiaperType
    }
    throw new Error(`Invalid diaper type: ${value}`)
}

function toDiaperColor(value: string | undefined | null): DiaperColor | undefined {
    if (Object.values(DiaperColor).includes(value as DiaperColor)) {
        return value as DiaperColor
    }
    return undefined
}

function toDiaperConsistency(value: string | undefined | null): DiaperConsistency | undefined {
    if (Object.values(DiaperConsistency).includes(value as DiaperConsistency)) {
        return value as DiaperConsistency
    }
    return undefined
}

function toDiaperSize(value: string | undefined | null): DiaperSize | undefined {
    if (Object.values(DiaperSize).includes(value as DiaperSize)) {
        return value as DiaperSize
    }
    return undefined
}

export { DiaperType, DiaperColor, DiaperConsistency, DiaperSize, toDiaperType, toDiaperColor, toDiaperConsistency, toDiaperSize }