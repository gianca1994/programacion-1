import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SensorComponent } from "./sensor/sensor.component"
import { AddNewSensorComponent } from './sensor/add-new-sensor/add-new-sensor.component';
import { EditSensorComponent } from './sensor/edit-sensor/edit-sensor.component';
import { UserComponent } from "./user/user.component"
import { LoginComponent } from './login/login.component';
import { AdminService as AuthAdminGuard } from "./auth/admin.service";

const routes: Routes = [

  {path: '', redirectTo: '/', pathMatch: 'full', data: { breadcrumb: 'Home' },},

  {
    path: '', data: { breadcrumb: 'Home' },
    children: [
      {
        path: 'login', data: { breadcrumb: 'Login' },
        children: [{
            path: '', component: LoginComponent,},],
      },
      
      {
        path: 'sensor', data: { breadcrumb: 'Sensor' },
        children: [{
            path: '', component: SensorComponent, canActivate: [AuthAdminGuard],},
          {
            path: 'add', component: AddNewSensorComponent, data: { breadcrumb: 'Add' }, canActivate: [AuthAdminGuard],},
          {
            path: 'edit/:id', component: EditSensorComponent, data: { breadcrumb: 'Edit' }, canActivate: [AuthAdminGuard],},],
      },

      {
        path: 'user',
        data: { breadcrumb: 'User' },
        children: [{
            path: '', component: UserComponent, canActivate: [AuthAdminGuard],},],
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
