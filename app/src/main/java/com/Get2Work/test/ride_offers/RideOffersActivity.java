package com.Get2Work.test.ride_offers;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Parcelable;
import android.support.annotation.DrawableRes;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.res.ResourcesCompat;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.text.Html;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.Get2Work.test.get_rides.GetRidesActivity;
import com.Get2Work.test.rides.RidesAdapter;
import com.Get2Work.test.util.Constant;
import com.google.common.collect.Lists;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.here.mobility.sdk.common.util.PermissionUtils;
import com.here.mobility.sdk.core.HereMobilitySdk;
import com.here.mobility.sdk.core.geo.Address;
import com.here.mobility.sdk.core.geo.LatLng;
import com.here.mobility.sdk.core.net.ResponseException;
import com.here.mobility.sdk.core.net.ResponseFuture;
import com.here.mobility.sdk.core.net.ResponseListener;
import com.here.mobility.sdk.demand.CreateRideRequest;
import com.here.mobility.sdk.demand.DemandClient;
import com.here.mobility.sdk.demand.PassengerDetails;
import com.here.mobility.sdk.demand.PublicTransportRideOffer;
import com.here.mobility.sdk.demand.Ride;
import com.here.mobility.sdk.demand.RideOffer;
import com.here.mobility.sdk.demand.RideOffersRequest;
import com.here.mobility.sdk.demand.RideStatusLog;
import com.here.mobility.sdk.demand.TaxiRideOffer;
import com.Get2Work.test.R;
import com.Get2Work.test.public_transport.PublicTransportActivity;
import com.Get2Work.test.ride_status.RideStatusActivity;
import com.here.mobility.sdk.map.FusedUserLocationSource;
import com.here.mobility.sdk.map.MapController;
import com.here.mobility.sdk.map.MapFragment;
import com.here.mobility.sdk.map.MapView;
import com.here.mobility.sdk.map.Marker;
import com.here.mobility.sdk.map.PolylineOverlay;
import com.here.mobility.sdk.map.geocoding.GeocodingResult;
import com.here.mobility.sdk.map.route.Route;


import java.util.ArrayList;
import java.util.Random;

/**********************************************************
 * Copyright © 2018 HERE Global B.V. All rights reserved. *
 **********************************************************/
public class RideOffersActivity extends AppCompatActivity implements MapView.MapReadyListener, RideOffersAdapter.RideOffersListener {


    /**
     * Taxi Ride offers list Intent.extra key.
     */
    private static final String EXTRA_TAXI_RIDE_OFFER_LIST = "TAXI_RIDE_OFFER_LIST";


    /**
     * Public transportation Ride offers list Intent.extra key.
     */
    private static final String EXTRA_PT_RIDE_OFFER_LIST = "PT_RIDE_OFFER_LIST";


    /**
     * Passenger details list Intent.extra key.
     */
    private static final String EXTRA_PASSENGER_DETAILS = "PASSENGER_DETAILS";


    private static final float MAP_ZOOM = 14.5f;
    private MapController mapController;
    /**
     * Location permission code.
     */
    private static final int LOCATION_PERMISSIONS_CODE = 42;
    private Marker pickupMarker;
    private Marker destinationMarker;

    /**
     * Use DemandClient to request ride.
     */
    private DemandClient demandClient;

    public static Integer selectedButton = 0;

    // Get2Work
    private FirebaseDatabase database;
    private DatabaseReference myRef;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ride_offers);
        demandClient = DemandClient.newInstance(this);

        //MapFragment initialization.
        MapFragment mapFragment = (MapFragment) getFragmentManager().findFragmentById(R.id.map_fragment);
        if (mapFragment != null) {
            mapFragment.loadMapAsync(this);
        }
        updateUI();
        // Get2Work
        ((TextView)findViewById(R.id.textView_rides_title)).setText( GetRidesActivity.custName );
        ((TextView)findViewById(R.id.textView_rides_adress)).setText( GetRidesActivity.addressText );
        database = FirebaseDatabase.getInstance();
        myRef = database.getReference("Here/" + HereMobilitySdk.getUserId() + "/ride");
        database.getReference("Here/"+ HereMobilitySdk.getUserId()).addValueEventListener(//addListenerForSingleValueEvent(
                new ValueEventListener() {
                    @Override
                    public void onDataChange(DataSnapshot dataSnapshot) {

                        String[] leaves = new String[4];
                        String[] prices = new String[4];
                        String[] times = new String[4];

                        leaves[0] = dataSnapshot.child("ride/taxi/leafs").getValue(String.class);
                        leaves[1] = dataSnapshot.child("ride/bus/leafs").getValue(String.class);
                        leaves[2] = dataSnapshot.child("ride/bike/leafs").getValue(String.class);
                        leaves[3] = dataSnapshot.child("ride/walk/leafs").getValue(String.class);

                        times[0] = dataSnapshot.child("ride/taxi/time").getValue(String.class);
                        times[1] = dataSnapshot.child("ride/bus/time").getValue(String.class);
                        times[2] = dataSnapshot.child("ride/bike/time").getValue(String.class);
                        times[3] = dataSnapshot.child("ride/walk/time").getValue(String.class);

                        ((TextView)findViewById(R.id.editText_1st))
                                .setText( results2string(0, leaves, times) ); //times[0] + " min.\n" + leaves[0] + " Leaves"
                        ((TextView)findViewById(R.id.editText_2nd))
                                .setText( results2string(1, leaves, times) );
                        ((TextView)findViewById(R.id.editText_3rd))
                                .setText( results2string(2, leaves, times) );
                        ((TextView)findViewById(R.id.editText_4th))
                                .setText( results2string(3, leaves, times) );

                    }

                    private String results2string(Integer idx, String[] leaves, String[] times){
                        return times[idx] + " min.\n" + leaves[idx] + " Leaves";
                    }

                    @Override
                    public void onCancelled(DatabaseError databaseError) {
                        //Log.w(TAG, "getUser:onCancelled", databaseError.toException());
                        // [START_EXCLUDE]
                        //setEditingEnabled(true);
                        // [END_EXCLUDE]
                    }
                });
    }


    /**
     * Update UI
     */
    private void updateUI(){
        RecyclerView rideOffersList = findViewById(R.id.ride_offers_list);
        RideOffersAdapter adapter = new RideOffersAdapter(this);
        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(this);
        rideOffersList.setLayoutManager(layoutManager);
        rideOffersList.setItemAnimator(new DefaultItemAnimator());
        rideOffersList.setAdapter(adapter);

        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setTitle(R.string.show_offers_title);
        }

        //Received ride offers list from Intent.extra and update the list.
        ArrayList<RideOffer> rideOffers = getRideOffers();
        adapter.updateDataSource(rideOffers);
    }


    /**
     * Called when ride offer did select.
     * @param offer selected {@link RideOffer}.
     */
    @Override
    public void offerItemSelected(@NonNull RideOffer offer) {
        offer.accept(new RideOffer.Visitor<Void>() {
            @Override
            public Void visit(@NonNull TaxiRideOffer taxiRideOffer) {
                requestRide(taxiRideOffer);
                return null;
            }

            @Override
            public Void visit(@NonNull PublicTransportRideOffer publicTransportRideOffer) {
                startActivity(PublicTransportActivity.createIntent(RideOffersActivity.this, publicTransportRideOffer));
                return null;
            }
        });
    }


    /**
     * Request to book Ride Offer.
     * @param taxiRideOffer An offer for ride. should be received from RideOffersRequest.
     */
    private void requestRide(@NonNull TaxiRideOffer taxiRideOffer){

        PassengerDetails passengerDetails = getPassengerDetails();

        if (passengerDetails != null) {
            
            CreateRideRequest rideRequest = CreateRideRequest.create(taxiRideOffer.getOfferId(), passengerDetails);

            //Request to book a ride.
            ResponseFuture<Ride> rideRequestFuture = demandClient.createRide(rideRequest);

            //Register for ride request updates.
            rideRequestFuture.registerListener(rideFutureListener);
        }
    }

    /**
     * Future ride listener. 
     */
    private ResponseListener<Ride> rideFutureListener = new ResponseListener<Ride>() {
        @Override
        public void onResponse(Ride ride) {
            startActivity(RideStatusActivity.createIntent(RideOffersActivity.this,ride));
            finish();
        }

        @Override
        public void onError(@NonNull ResponseException e) {
            Toast.makeText(RideOffersActivity.this, e.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
        }
    };


    @Override
    protected void onDestroy() {
        super.onDestroy();

        //It's important to call shutdown function when the client is no longer needed.
        if (demandClient != null) {
            demandClient.shutdownNow();
        }
    }


    /**
     * Getter. Extra list of ride offers
     * @return list of ride offers
     * @throws RuntimeException In case RideOffer list is empty or null.
     */
    @NonNull
    private ArrayList<RideOffer> getRideOffers(){
        ArrayList<RideOffer> rideOffers = Lists.newArrayList();
        if (getIntent().hasExtra(EXTRA_TAXI_RIDE_OFFER_LIST)){
            rideOffers.addAll(getIntent().getParcelableArrayListExtra(EXTRA_TAXI_RIDE_OFFER_LIST));
        }
        if (getIntent().hasExtra(EXTRA_PT_RIDE_OFFER_LIST)){
            rideOffers.addAll(getIntent().getParcelableArrayListExtra(EXTRA_PT_RIDE_OFFER_LIST));
        }

        if (rideOffers.size() == 0){
            throw new RuntimeException("Ride offer list is mandatory for starting RideOffersActivity");
        }
        return rideOffers;
    }


    /**
     * Getter. Extra PassengerDetails.
     * @return ride PassengerDetails.
     */
    @Nullable
    private PassengerDetails getPassengerDetails(){
        PassengerDetails passengerDetails= null;
        if (getIntent().hasExtra(EXTRA_PASSENGER_DETAILS)){
            passengerDetails = getIntent().getParcelableExtra(EXTRA_PASSENGER_DETAILS);
        }
        return passengerDetails;
    }


    /**
     * A Helper method, The main task of this Activity is to request Ride Offers and book selected offer.
     * PassengerDetails needed to creating ride after ride offer selected.
     * @param context The context of the sender.
     * @param taxiRideOffers list of TaxiRideOffer object, received from {@link DemandClient#getRideOffers(RideOffersRequest)}
     * @param ptRideRequest list of PublicTransportRideOffer object, received from {@link DemandClient#getRideOffers(RideOffersRequest)}
     * @param passengerDetails PassengerDetails of user.
     * @return An Intent to RideOffersActivity with safe pass params.
     */
    @NonNull
    public static Intent createIntent(Context context,
                                      @NonNull ArrayList<TaxiRideOffer> taxiRideOffers,
                                      @NonNull ArrayList<PublicTransportRideOffer> ptRideRequest,
                                      @NonNull PassengerDetails passengerDetails){
        Intent intent = new Intent(context,RideOffersActivity.class);
        intent.putParcelableArrayListExtra(EXTRA_TAXI_RIDE_OFFER_LIST,taxiRideOffers);
        intent.putParcelableArrayListExtra(EXTRA_PT_RIDE_OFFER_LIST,ptRideRequest);
        intent.putExtra(EXTRA_PASSENGER_DETAILS,passengerDetails);
        return intent;
    }

    public void onAnyButtonClicked(@NonNull View view) {

        //Toast.makeText(this, "This is my Toast message!",
        //        Toast.LENGTH_LONG).show();

        //((ImageView)findViewById(R.id.imageView_1st)).setImageResource(R.drawable.bus);

        if (view.getId()==R.id.editText_1st){
            selectedButton = 1;
            myRef.child("/bike/used").setValue("0");
            myRef.child("/bus/used").setValue("0");
            //myRef.child("/taxi/used").setValue("0");
            myRef.child("/walk/used").setValue("0");
        }
        else if (view.getId()==R.id.editText_2nd){
            selectedButton = 2;
            myRef.child("/bike/used").setValue("0");
            //myRef.child("/bus/used").setValue("0");
            myRef.child("/taxi/used").setValue("0");
            myRef.child("/walk/used").setValue("0");
        }
        else if (view.getId()==R.id.editText_3rd){
            selectedButton = 3;
            //myRef.child("/bike/used").setValue("0");
            myRef.child("/bus/used").setValue("0");
            myRef.child("/taxi/used").setValue("0");
            myRef.child("/walk/used").setValue("0");
        }
        else if (view.getId()==R.id.editText_4th){
            selectedButton = 4;
            myRef.child("/bike/used").setValue("0");
            myRef.child("/bus/used").setValue("0");
            myRef.child("/taxi/used").setValue("0");
            //myRef.child("/walk/used").setValue("0");
        }

        /*
        String styledText = "<b>Bus</b><br>60 min, 30 Leaves" +
                String.format("<img src=\"%s\"/>", R.drawable.leaf);
        ((TextView)findViewById(R.id.editText_1st))
                .setText( Html.fromHtml( styledText ) );

        styledText = String.format("<img src=\"%s\"/>", R.drawable.leaf);
        //((ImageView)findViewById(R.id.imageView_2nd)).setImageResource(R.drawable.leaf);
        ((TextView)findViewById(R.id.editText_2nd))
                .setText( Html.fromHtml( styledText ) );
        */
        findViewById(getResources().getIdentifier("book_button", "id", getPackageName()))
                .callOnClick();
    }

    /**
     * this callback is called when the map is set-up, before we render any tiles to the screen - so this is the place to set those values
     * @param mapController map controller to interact with the map.
     */
    @Override
    public void onMapReady(@NonNull MapController mapController) {
        this.mapController = mapController;
        // LatLng pickup = LatLng.fromDegrees( 51.50341,-0.12765);
        // LatLng destination = LatLng.fromDegrees( 51.456032, -0.076303);
        LatLng pickup = GetRidesActivity.fromLatLong;
        LatLng destination = GetRidesActivity.toLatLong;
        mapController.setPosition(pickup);
        showPickupMarkerAt(pickup);
        showDestinationMarkerAt(destination);
        //Set the map center position.
        //mapController.setPosition(Constant.CENTER_OF_LONDON);
        //Set map zoom.
        mapController.setZoom(MAP_ZOOM);
        //Log.i("GUY", ""+ GetRidesActivity.route1.getDistance());
        Route route = GetRidesActivity.route1;
        long routePolylineId = mapController.addPolyline(new PolylineOverlay(route.getGeometry()));
        mapController.showBoundingBox(route.getGeometry().getBoundingBox(),new Rect(20, 180, 20, 70));

        //Log.i("GUY", "GUY: ");
        if (!PermissionUtils.hasAnyLocationPermissions(this)) {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION}, LOCATION_PERMISSIONS_CODE);
        }else{
            //startLocationUpdates();
        }
    }


    @Override
    public void onMapFailure(@NonNull Exception e) {
        Log.e("RideOffersActivity", "onMapFailure: ", e);
    }

    /**
     * Start user location updates.
     */
    @SuppressLint("MissingPermission")
    private void startLocationUpdates(){

        mapController.getUserLocationMarkerManager().setLocationSource(new FusedUserLocationSource(this));

    }

    /**
     * Creates a marker at the given location.
     * @param location the marker location
     * @param imageRes image res of marker icon.
     * @return Marker
     */
    @NonNull
    private Marker createMarker(@NonNull LatLng location, @DrawableRes int imageRes){

        //Create map marker.
        Marker marker = mapController.addMarker();
        Resources resources = getResources();
        Drawable drawable = ResourcesCompat.getDrawable(resources, imageRes, null);
        if (drawable == null){
            throw new Resources.NotFoundException();
        }

        //Set marker style.
        int width = drawable.getIntrinsicWidth();
        int height = drawable.getIntrinsicHeight();
        float density = resources.getDisplayMetrics().density;
        String size = "[" + Math.round(width/density) + "px, " + Math.round(height/density) + "px]";
        String styleString = "{ style: 'points', color: 'white', size: " + size + ", order: 10000, collide: false, anchor: top }";
        marker.setStylingFromString(styleString);

        //Set marker icon
        marker.setDrawable(drawable);

        //Set marker location
        marker.setPoint(location);

        return marker;
    }


    /**
     * Show pickup marker at point.
     * @param point the point.
     */
    public void showPickupMarkerAt(@NonNull LatLng point){
        if (pickupMarker == null){
            // Create marker lazily.
            pickupMarker = createMarker(point, R.drawable.ic_location_on_black_24dp);
        }else{
            // Otherwise just set marker location.
            pickupMarker.setPoint(point);
        }
    }


    /**
     * Show pickup marker at point.
     * @param point the point.
     */
    public void showDestinationMarkerAt(@NonNull LatLng point){
        if (destinationMarker == null) {
            // Create marker lazily.
            destinationMarker = createMarker(point, R.drawable.ic_pin_drop_black_24dp);
        }else{
            // Otherwise just set marker location.
            destinationMarker.setPoint(point);
        }
    }
}