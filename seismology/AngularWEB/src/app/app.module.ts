import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { InterceptorService } from './auth/interceptor.service';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SensorComponent } from './sensor/sensor.component';
import { LoginComponent } from './login/login.component';
import { UserComponent } from './user/user.component';
import { AddNewSensorComponent } from './sensor/add-new-sensor/add-new-sensor.component';
import { EditSensorComponent } from './sensor/edit-sensor/edit-sensor.component';
import { DeleteSensorComponent } from './sensor/delete-sensor/delete-sensor.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';


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
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: InterceptorService,
    multi: true
  },],

  bootstrap: [AppComponent]
})
export class AppModule { }
