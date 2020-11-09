import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service';
import jwt_decode from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})

export class AdminService implements CanActivate {

  constructor(public auth: AuthService, public router: Router) { }

  canActivate(): boolean {

    if (this.auth.isAuthenticated) {
      const token = localStorage.getItem('token');
      const token_decode = jwt_decode(token);
      console.log(token_decode);
      if (token_decode.user_claims.admin) {
        return true;}}

    this.router.navigate(['login']);
    return false;}
}
