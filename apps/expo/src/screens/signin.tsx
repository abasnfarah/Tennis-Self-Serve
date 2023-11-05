import React from "react";

import { View, SafeAreaView } from "react-native";

import SignInWithOAuth from "../components/SignInWithOAuth";

export const SignInSignUpScreen = () => {
  return (
    <SafeAreaView className="bg-[#f5eac8] bg-gradient-to-b from-[#2e026d] to-[#b4ad92]">
      <View className="h-full w-full p-4">
        <SignInWithOAuth />
      </View>
    </SafeAreaView>
  );
};
