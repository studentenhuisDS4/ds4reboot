export interface IReceipt {
    receipt_cost: number;
    receipt_costs_split: IReceiptCost[];
}

export interface IReceiptCost {
    cost_user: number;
    affected_user_id: number;
}
