import React from "react";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { TRPCProvider } from "./utils/trpc";
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from '@expo/vector-icons/Ionicons';

import { HomeScreen } from "./screens/home";
import { CameraScreen } from "./screens/camera";
import { InfoScreen } from "./screens/tennisinfo";
import { SignInSignUpScreen } from "./screens/signin";
import { ClerkProvider, SignedIn, SignedOut } from "@clerk/clerk-expo";
import { tokenCache } from "./utils/cache";
import Constants from "expo-constants";

const Tab = createBottomTabNavigator();

function MyTabs() {
  return (
    <Tab.Navigator screenOptions={{headerShown: false}}>
      <Tab.Screen name="Home" component={HomeScreen} options={{
        tabBarLabel: 'Home',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="home" color={color} size={size} />
        ),
    }}/>
      <Tab.Screen name="Camera" component={CameraScreen} options={{
        tabBarLabel: 'Camera',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="camera" color={color} size={size} />
        ),
    }}/>
      <Tab.Screen name="Tennis Info" component={InfoScreen} options={{
        tabBarLabel: 'Tennis Info',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="tennisball" color={color} size={size} />
        ),
    }}/>
    </Tab.Navigator>
  );
}

export const App = () => {
  return (
    <ClerkProvider
      publishableKey={Constants.expoConfig?.extra?.CLERK_PUBLISHABLE_KEY}
      tokenCache={tokenCache}
    >
      <SignedIn>
        <TRPCProvider>
          <SafeAreaProvider>
            <NavigationContainer>
              <MyTabs />
            </NavigationContainer>
          </SafeAreaProvider>
        </TRPCProvider>
      </SignedIn>
      <SignedOut>
        <SignInSignUpScreen />
      </SignedOut>
    </ClerkProvider>
  );
};
