package com.Get2Work.test;

import android.support.multidex.MultiDexApplication;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.here.mobility.sdk.core.HereMobilitySdk;


/**********************************************************
 * Copyright © 2018 HERE Global B.V. All rights reserved. *
 **********************************************************/
public class SampleApplication extends MultiDexApplication {


    @Override
    public void onCreate() {
        super.onCreate();

        //HereMobilitySdk initialization must be called in onCreate() method to initialize the SDK.
        HereMobilitySdk.init(this);

        //Returns whether the current process is the SDK agent process.
        if (HereMobilitySdk.isHereAgentProcess(this)){
            return;
        }

        //put here the rest of you app sdks initialization.
        // Write a message to the database
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference myRef = database.getReference("message");

        myRef.setValue("Damn, San Fransisco!");
    }
}