import { Text, View, Button } from 'react-native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaView } from "react-native-safe-area-context";
import YoutubePlayer from 'react-native-youtube-iframe';
import React from "react";

export const TennisInfo = ({navigation}: any) => {
  return (
    <SafeAreaView className="bg-[#f5eac8] bg-gradient-to-b from-[#2e026d] to-[#b4ad92]">
      <View className="h-full w-full p-4">
        <Text style={{fontSize: 30, fontWeight: 'bold'}}>Serve Tutorials</Text> 
          <View style={{alignItems: 'center', justifyContent: 'center'}}>
            <Text>Go to Beginner Serve Tutorial</Text>
            <Button
              title="Beginner Serve Tutorial"
              onPress={() => navigation.navigate('Beginner')}
              color={'#00ca73'}
            />
            <Text>Go to Racket Grip Tutorial</Text>
            <Button
              title="Racket Grip Tutorial"
              onPress={() => navigation.navigate('Grip')}
              color={'#00ca73'}
            />
          </View>
        <Text style={{fontSize: 30, fontWeight: 'bold',alignItems: 'center', justifyContent: 'center'}}>Professional Serves</Text> 
          <View style={{alignItems: 'center', justifyContent: 'center'}}>
              <Text>Go to Roger Federer Serving</Text>
              <Button
                title="Roger Federer Serving"
                onPress={() => navigation.navigate('Roger')}
                color={'#00ca73'}
              />
              <Text>Go to Novak Djokovic Serving</Text>
              <Button
                title="Novak Djokovic Serving"
                onPress={() => navigation.navigate('Novak')}
                color={'#00ca73'}
              />
              <Text>Go to Nick Kyrgios Serving</Text>
              <Button
                title="Nick Kyrgios Serving"
                onPress={() => navigation.navigate('Nick')}
                color={'#00ca73'}
              />
          </View>
      </View>
    </SafeAreaView>
  );
}

export const Roger = () => {
  return (
    <SafeAreaView className="bg-[#f5eac8] bg-gradient-to-b from-[#2e026d] to-[#b4ad92]">
      <View className="h-full w-full p-4">
        <Text style={{fontSize: 30, fontWeight: 'bold'}}>Roger Federer Serving</Text> 
          <YoutubePlayer
              height={200}
              play={false}
              videoId={'mKXtVQnqhB4'}
            />
      </View>
    </SafeAreaView>
  );
}
export const Novak = () => {
  return (
    <SafeAreaView className="bg-[#f5eac8] bg-gradient-to-b from-[#2e026d] to-[#b4ad92]">
      <View className="h-full w-full p-4">
        <Text style={{fontSize: 30, fontWeight: 'bold'}}>Novak Djokovic Serving</Text>  
          <YoutubePlayer
            height={200}
            play={false}
            videoId={'FuDJ7crbkBo'}
          />
      </View>
    </SafeAreaView>
  );
}
export const Nick = () => {
  return (
    <SafeAreaView className="bg-[#f5eac8] bg-gradient-to-b from-[#2e026d] to-[#b4ad92]">
      <View className="h-full w-full p-4">
        <Text style={{fontSize: 30, fontWeight: 'bold'}}>Nick Kyrgios Serving</Text>  
          <YoutubePlayer
            height={200}
            play={false}
            videoId={'Z_LU2q1CROA'}
          />
      </View>
    </SafeAreaView>

  );
}
export const Beginner = () => {
  return (
    <SafeAreaView className="bg-[#f5eac8] bg-gradient-to-b from-[#2e026d] to-[#b4ad92]">
      <View className="h-full w-full p-4">
        <Text style={{fontSize: 30, fontWeight: 'bold'}}>Beginner Tutorial</Text> 
          <YoutubePlayer
            height={200}
            play={false}
            videoId={'FKtqaKjZVPs'}
          />
      </View>
    </SafeAreaView>
  );
}

export const Grip = () => {
  return (
    <SafeAreaView className="bg-[#f5eac8] bg-gradient-to-b from-[#2e026d] to-[#b4ad92]">
      <View className="h-full w-full p-4">
        <Text style={{fontSize: 30, fontWeight: 'bold'}}>How to Grip Racket</Text> 
          <YoutubePlayer
            height={200}
            play={false}
            videoId={'qbBHq6-G3Rc'}
          />
      </View>
    </SafeAreaView>
  );
}

const Stack = createNativeStackNavigator();

export const InfoScreen = () => {
  return (
      <Stack.Navigator initialRouteName="TennisInfo" screenOptions={{headerShown: true}}>
        <Stack.Screen name="TennisInfo" component={TennisInfo} />
        <Stack.Screen name="Beginner" component={Beginner} /> 
        <Stack.Screen name="Roger" component={Roger} />
        <Stack.Screen name="Novak" component={Novak} />
        <Stack.Screen name="Nick" component={Nick} />
        <Stack.Screen name="Grip" component={Grip} />
      </Stack.Navigator>
  );
}