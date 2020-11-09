import { User } from "../user/user.model";

export interface ISensor {
  id: number;
  name: string;
  status: boolean;
  active: boolean;
  ip?: string;
  port?: number;
  user?: User;
  user_id?: number;
}

export class Sensor implements ISensor {
  constructor(
    public id: number, public name: string, public status: boolean, public active: boolean,
        public user_id?: number, public ip?: string, public port?: number, public user?: User,
  ){}
}