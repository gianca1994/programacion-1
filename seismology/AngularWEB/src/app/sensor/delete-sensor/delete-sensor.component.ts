import { Component, OnInit } from '@angular/core';
import { Sensor } from "../sensor.model"

@Component({
  selector: 'app-delete-sensor',
  templateUrl: './delete-sensor.component.html',
  styleUrls: ['./delete-sensor.component.scss']
})
export class DeleteSensorComponent implements OnInit {

  @Input() sensor: Sensor;

  constructor() { }

  ngOnInit(): void {
  }

}
