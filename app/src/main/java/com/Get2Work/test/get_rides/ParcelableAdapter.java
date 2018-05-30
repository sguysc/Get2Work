package com.Get2Work.test.get_rides;

import android.os.Parcelable;

import com.google.gson.*;
import java.lang.reflect.Type;

public class ParcelableAdapter implements JsonSerializer<Parcelable>, JsonDeserializer<Parcelable> {

    @Override
    public JsonElement serialize(Parcelable src, Type typeOfSrc, JsonSerializationContext context) {
        JsonObject result = new JsonObject();
        result.add("type", new JsonPrimitive(src.getClass().getSimpleName()));
        result.add("properties", context.serialize(src, src.getClass()));

        return result;
    }

    @Override
    public Parcelable deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context)
        throws JsonParseException {
        JsonObject jsonObject = json.getAsJsonObject();
        String type = jsonObject.get("type").getAsString();
        JsonElement element = jsonObject.get("properties");

        try {
            return context.deserialize(element, Class.forName("com.here.mobility.sdk.map." + type));
        } catch (ClassNotFoundException cnfe) {
            throw new JsonParseException("Unknown element type: " + type, cnfe);
        }
    }
}
