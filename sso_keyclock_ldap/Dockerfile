# Use the SDK image for build and base image for runtime
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

# Install the required LDAP libraries (do this in the build stage for cache efficiency)
RUN apt-get update && \
    apt-get install -y libldap-dev libsasl2-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /src

# Copy the project file and restore dependencies
COPY ["sso_keyclock_ldap.csproj", "./"]
RUN dotnet restore "./sso_keyclock_ldap.csproj"

# Copy the rest of the application and build it
COPY . .
RUN dotnet publish "./sso_keyclock_ldap.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Use the base runtime image for the final image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final

# Set the working directory for runtime
WORKDIR /app

# Expose necessary ports
EXPOSE 8080 8081

# Copy the published output from the build stage
COPY --from=build /app/publish .

# Set the entry point to start the application
ENTRYPOINT ["dotnet", "sso_keyclock_ldap.dll"]


# ##original image
# # Use the base image for ASP.NET
# FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base

# # Install the required LDAP libraries
# RUN apt-get update && apt-get install -y libldap-dev libsasl2-dev && apt-get upgrade -y

# # Set the working directory and expose necessary ports
# USER app
# WORKDIR /app
# EXPOSE 8080
# EXPOSE 8081

# # Use the SDK image for build
# FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
# ARG BUILD_CONFIGURATION=Release
# WORKDIR /src

# # Copy the project file and restore dependencies
# COPY ["sso_keyclock_ldap.csproj", "."]
# RUN dotnet restore "./sso_keyclock_ldap.csproj"

# # Copy the rest of the application and build it
# COPY . . 
# WORKDIR "/src/."
# RUN dotnet build "./sso_keyclock_ldap.csproj" -c $BUILD_CONFIGURATION -o /app/build

# # Publish the application
# FROM build AS publish
# ARG BUILD_CONFIGURATION=Release
# RUN dotnet publish "./sso_keyclock_ldap.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

# # Final stage to create the runtime image
# FROM base AS final
# WORKDIR /app

# # Copy the published output from the previous stage
# COPY --from=publish /app/publish .

# # Set the entry point to start the application
# ENTRYPOINT ["dotnet", "sso_keyclock_ldap.dll"]
