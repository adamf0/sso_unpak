##optimize image 
# Use the SDK image for build (this is needed for building the app)
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release

# Install the required LDAP libraries, upgrade the system and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends libldap-dev libsasl2-dev && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory for the build stage
WORKDIR /src

# Copy the project file and restore dependencies
COPY ["sso_keyclock_ldap.csproj", "."]
RUN dotnet restore "./sso_keyclock_ldap.csproj"

# Copy the rest of the application and build it
COPY . . 
WORKDIR "/src/."
RUN dotnet build "./sso_keyclock_ldap.csproj" -c $BUILD_CONFIGURATION -o /app/build

# Publish the application (only necessary files)
FROM build AS publish
RUN dotnet publish "./sso_keyclock_ldap.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

# Use a slim .NET runtime base image to reduce the size of the final image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base

# Set the working directory for the final runtime image
WORKDIR /app

# Copy only the published output from the build stage
COPY --from=publish /app/publish .

# Expose necessary ports
EXPOSE 8080
EXPOSE 8081

# Set the entry point to start the application
ENTRYPOINT ["dotnet", "sso_keyclock_ldap.dll"]

##original image
# # Use the base image for ASP.NET
# FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base

# # Install the required LDAP libraries
# RUN apt-get update && apt-get install -y libldap-dev libsasl2-dev

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
