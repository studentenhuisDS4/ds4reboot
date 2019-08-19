export interface ITokenClaims {
    user_id: number;
    exp: Date;
    orig_iat: Date;
    email: string;
    username: string;
}
