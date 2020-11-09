import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  password="";
  email="";

  constructor(private authService: AuthService) {}

  login(){this.authService.login(this.password, this.email)}
  
  ngOnInit(): void {}
}
