import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddNewSensorComponent } from './add-new-sensor.component';

describe('AddNewSensorComponent', () => {
  let component: AddNewSensorComponent;
  let fixture: ComponentFixture<AddNewSensorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddNewSensorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddNewSensorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
