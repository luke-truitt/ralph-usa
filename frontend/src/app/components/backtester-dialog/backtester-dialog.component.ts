import { Component, OnInit, Inject } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { MatDatepicker, MatError, MatTooltip } from '@angular/material'
import { FormControl } from '@angular/forms'

import { DataService } from '../../services/data.service';



@Component({
  selector: 'app-backtester-dialog',
  templateUrl: './backtester-dialog.component.html',
  styleUrls: ['./backtester-dialog.component.css']
})
export class BacktesterDialogComponent implements OnInit {

  fullName:string;
  birthDate:Date;
  retirementDate:Date;
  targetReturn:number;

  closingStrategy:any[] = [
    {value:'threshold', viewValue:'Sell When Thresholds are Reached'},
    {value:'daily', viewValue:'Sell Everyday at Close'}
  ];

  selectedClosingStrategy:string;
  startDate:Date;
  endDate:Date;
  portfolioValue:number;

  models:any[];

  selectedModel:string;

  inputError:boolean = false;

  minStartDate:Date;
  maxStartDate:Date;
  minEndDate:Date;
  maxEndDate:Date;

  // start date, end date, portfolio values, a trading algorithm (but you'll need to find a nice way to display the
  // possible trading algorithms i.e. show all the parameters in them so they know) and then what other things you want to plot
  // (SNP, Oil, a different portfolio)

  constructor(private dataService:DataService, public dialogRef: MatDialogRef<BacktesterDialogComponent>, @Inject(MAT_DIALOG_DATA) private data) { }

  ngOnInit() {
    this.minStartDate = new Date(this.data['firstDate'])
    this.maxEndDate = new Date(this.data['endDate']);
    this.models = this.data['models']
    this.maxStartDate = this.subtractDays(this.maxEndDate, 1);

    // eventually move this to backend
    this.modelParamsToStrings();
  }
  modelParamsToStrings() {
    let paramsStrings = [];
    this.models.forEach(element => {

      let paramsString = ''
      element['parameters'].forEach(item => {
        paramsString = paramsString + item['name'] + ': ' + item['value']  + '    |    '
      })
      element['paramsString'] = paramsString.substr(0,paramsString.length-2);
    });
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  onSubmit():void{
    // validate data, throw error if necessary, otherwise return to other component

    if(this.startDate == null || this.endDate == null ||
      this.startDate.getTime() >= this.endDate.getTime() || isNaN(Number(this.portfolioValue)) || this.selectedModel == null){
      this.inputError = true;
      return;
    }
    let modelId = "";

    this.models.forEach( model => {
      if(model['name'] == this.selectedModel){
        modelId = model['id'];
      }
    });

    this.dialogRef.close({'startDate': this.startDate, 'endDate': this.endDate, 'portfolioValue': this.portfolioValue, 'model': modelId, 'target_return': this.targetReturn, 'closing_strategy': this.selectedClosingStrategy, 'name': this.fullName, 'retirementDate':this.retirementDate, 'birthDate':this.birthDate});
  }

  onDemo():void{
    // Demo

    this.dialogRef.close({'startDate': new Date('3/4/2019'), 'endDate': new Date('4/6/2019'), 'portfolioValue': 1000000, 'model': '6ae7528c-5f71-41ab-9c7f-139f1b3ff45e', 'target_return': 0.02, 'closing_strategy': 'threshold', 'name': 'Dr. Henry Pfister', 'retirementDate': new Date('10/26/2030'), 'birthDate': new Date('10/26/1970')});
  }

  updateBirthDate($event){
    this.inputError = false;
    this.birthDate = new Date($event['value']);
  }

  updateRetireDate($event){
    this.inputError = false;
    this.retirementDate = new Date($event['value']);
  }


  updateStartDate($event){
    this.inputError = false;
    this.startDate = new Date($event['value']);
    this.minEndDate = this.subtractDays(new Date(this.startDate), -1);
  }

  updateEndDate($event){
    this.inputError = false;
    this.endDate = new Date($event['value']);
  }

  updateModel($event){
    this.inputError = false;
    this.selectedModel = $event['value'];
  }

  updateCloseType($event){
    this.inputError = false;
    this.selectedClosingStrategy = $event['value'];
  }

  subtractDays(date:Date, days:number){
    let tempDate = new Date();
    tempDate.setTime(date.getTime() - (days*24*60*60*1000));
    return tempDate;
}

}
