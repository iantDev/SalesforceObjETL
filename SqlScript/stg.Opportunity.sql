create table stg.Opportunity (
    tblId serial,
    Id char(18) Null,
    IsDeleted boolean Null,
    AccountId varchar (255) Null,
    Name varchar (255) Null,
    Description varchar (4000) Null,
    StageName varchar (255) Null,
    Amount NUMERIC (16,2) Null,
    Probability numeric(5,2) Null,
    CloseDate date Null,
    Type varchar (255) Null,
    NextStep varchar (255) Null,
    LeadSource varchar (255) Null,
    IsClosed boolean Null,
    IsWon boolean Null,
    ForecastCategory varchar (255) Null,
    ForecastCategoryName varchar (255) Null,
    CampaignId varchar (255) Null,
    HasOpportunityLineItem boolean Null,
    Pricebook2Id varchar (255) Null,
    OwnerId varchar (255) Null,
    CreatedDate timestamp with time zone Null,
    CreatedById varchar (255) Null,
    LastModifiedDate timestamp with time zone Null,
    LastModifiedById varchar (255) Null,
    SystemModstamp timestamp with time zone Null,
    LastActivityDate date Null,
    FiscalQuarter int Null,
    FiscalYear int Null,
    Fiscal varchar (255) Null,
    ContactId varchar (255) Null,
    LastViewedDate timestamp with time zone Null,
    LastReferencedDate timestamp with time zone Null,
    SyncedQuoteId varchar (255) Null,
    HasOpenActivity boolean Null,
    HasOverdueTask boolean Null,
    Opportunity_Shortname__c varchar (255) Null,
    Contract_Term__c numeric Null,
    Account_Shortname__c varchar (255) Null,
    Total_Contract_Amount__c NUMERIC (16,2) Null,
    Total_Price_per_Room__c NUMERIC (16,2) Null,
    Activity_Monitor__c varchar (255) Null,
    Days_Since_Last_Activity__c numeric Null,
    Payment_Terms__c varchar (255) Null,
    Feature_Request__c varchar (4000) Null,
    Main_Sales_Product_Driver__c varchar (255) Null,
    Subscription_Start_Date__c date Null,
    Projected_Revenue__c NUMERIC (16,2) Null,
    Mirrors__c numeric Null,
    Pricing_Notes__c varchar (4000) Null,
    Renewal_Notes__c varchar (4000) Null,
    Product_s__c varchar (4000) Null,
    Competitor__c varchar (255) Null,
    Closed_Lost_Reason__c varchar (4000) Null,
    Account_Name__c varchar (255) Null,
    Integration_s__c varchar (4000) Null,
    Tablets__c numeric Null,
    Install_Date__c date Null,
    Services__c NUMERIC (16,2) Null,
    Sales_Booking_Amount__c NUMERIC (16,2) Null,
    Hardware_Amount__c NUMERIC (16,2) Null,
    Agreement_Type__c varchar (4000) Null,
    LastActivityDate__c date Null,
    Renewal_Term__c varchar (255) Null,
    Software_Amount__c NUMERIC (16,2) Null,
    Monthly_Recurring_Revenue__c NUMERIC (16,2) Null,
    CLOSED_reasons__c varchar (4000) Null,
    Initial_Contract_Term__c varchar (255) Null,
    Termination_Date_Services__c date Null,
    End_Date__c date Null,
    Software_License__c NUMERIC (16,2) Null,
    Subscription__c NUMERIC (16,2) Null,
    End_DateSFDC__c date Null,
    Echos__c numeric Null,
    Project_Status__c varchar (255) Null,
    Hotel_Renewal_Notice__c numeric Null,
    Send_Renewal_Email_Notification__c date Null,
    Per_Room_Per_Day__c NUMERIC (16,2) Null,
    Chromecast__c numeric Null,
    Deployment_Type__c varchar (255) Null,
    SDR__c varchar (255) Null,
    Closed_Lost_Other_Reason_Tex__c varchar (4000) Null,
    Number_of_Rooms__c numeric Null,
    CONSTRAINT PK_stg_Opportunity PRIMARY KEY(id, SystemModstamp)
)