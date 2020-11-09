import { Component, OnInit } from '@angular/core';
import { Sensor } from "./sensor.model"
import { SensorService } from './sensor.service';

@Component({
  selector: 'app-sensor', templateUrl: './sensor.component.html', styleUrls: ['./sensor.component.scss']
})

export class SensorComponent implements OnInit {

  selectedSensor: Sensor;
  sensors: Sensor[];

  constructor(private sensorService: SensorService) { }

  ngOnInit(): void {
    this.getSensors();}

  getSensors(): void {
    this.sensorService.getSensors().subscribe(sensors => this.sensors = sensors["sensors"]);}

  onSelect(sensor: Sensor): void {
    this.selectedSensor = sensor;}

  delete(sensor: Sensor): void {
    this.sensorService.deleteSensor(sensor.id).subscribe(data => {this.getSensors();})}
}
