import { Injectable } from '@angular/core';
import { Sensor } from "./sensor.model"
import { Observable, of } from 'rxjs';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { API_URL } from '../env';

@Injectable({
  providedIn: 'root'
})

export class SensorService {

  constructor(private http: HttpClient) { }

  getSensors(): Observable<Sensor[]> {
    return this.http.get<Sensor[]>(API_URL + '/sensors');}

  deleteSensor(id) {
    return this.http.delete<Sensor>(API_URL + '/sensor/' + id);}
    
  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'The request could not be completed');}
}
