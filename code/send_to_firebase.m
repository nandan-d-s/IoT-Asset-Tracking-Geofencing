function send_to_firebase(latitude, longitude, status, distance)
    % Firebase URL
    url = 'https://your-firebase-database.firebaseio.com/asset1.json';

    % Create structured data with geofence status
    data.latitude = latitude;
    data.longitude = longitude;
    data.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
    data.status = status;
    data.distance = distance;

    % Send to Firebase
    try
        response = webwrite(url, data);
        disp("✅ Data sent to Firebase successfully:");
        disp(response);
    catch ME
        disp("❌ Failed to send data to Firebase:");
        disp(getReport(ME));
    end
end