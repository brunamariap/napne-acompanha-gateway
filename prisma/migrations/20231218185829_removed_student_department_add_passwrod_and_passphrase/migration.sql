/*
  Warnings:

  - The values [STUDENT] on the enum `Departments` will be removed. If these variants are still used in the database, this will fail.
  - Added the required column `passphrase` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `password` to the `User` table without a default value. This is not possible if the table is not empty.

*/
-- AlterEnum
BEGIN;
CREATE TYPE "Departments_new" AS ENUM ('TEACHER', 'ADMINISTRATOR');
ALTER TABLE "User" ALTER COLUMN "department" TYPE "Departments_new" USING ("department"::text::"Departments_new");
ALTER TYPE "Departments" RENAME TO "Departments_old";
ALTER TYPE "Departments_new" RENAME TO "Departments";
DROP TYPE "Departments_old";
COMMIT;

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "passphrase" TEXT NOT NULL,
ADD COLUMN     "password" TEXT NOT NULL;
