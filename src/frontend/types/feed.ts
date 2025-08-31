enum BreastFeedSide {
    Left = 'left',
    Right = 'right',
    Both = 'both'
}

function toBreastFeedSide(value: string): BreastFeedSide {
    if (Object.values(BreastFeedSide).includes(value as BreastFeedSide)) {
        return value as BreastFeedSide;
    }
    throw new Error(`Invalid breast feed side: ${value}`);
}

export { BreastFeedSide, toBreastFeedSide }