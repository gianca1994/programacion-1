import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SensorComponent } from './sensor/sensor/sensor.component';
import { LoginComponent } from './login/login/login.component';
import { UserComponent } from './user/user/user.component';
import { AddNewSensorComponent } from './sensor/add-new-sensor/add-new-sensor.component';
import { EditSensorComponent } from './sensor/edit-sensor/edit-sensor.component';
import { DeleteSensorComponent } from './sensor/delete-sensor/delete-sensor.component';

@NgModule({
  declarations: [
    AppComponent,
    SensorComponent,
    LoginComponent,
    UserComponent,
    AddNewSensorComponent,
    EditSensorComponent,
    DeleteSensorComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
