-- CreateEnum
CREATE TYPE "Departments" AS ENUM ('TEACHER', 'STUDENT', 'ADMINISTRATOR');

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "registration" TEXT NOT NULL,
    "picture" TEXT NOT NULL,
    "department" "Departments" NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);
