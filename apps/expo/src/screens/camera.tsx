import { Text, View } from 'react-native';
import React from "react";
import RecordVideo from '../components/RecordVideo';

export const CameraScreen = () => {
  return (
    <View style={{flex: 1}}>
      <RecordVideo />
    </View>
  );
}
