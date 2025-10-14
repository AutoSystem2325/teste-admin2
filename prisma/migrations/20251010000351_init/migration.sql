-- CreateTable
CREATE TABLE "maes" (
    "id" TEXT NOT NULL,
    "nome" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "senha" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "maes_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "filhos" (
    "id" TEXT NOT NULL,
    "nome" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "senha" TEXT NOT NULL,
    "validade" TIMESTAMP(3) NOT NULL,
    "maeId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "filhos_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "maes_email_key" ON "maes"("email");

-- CreateIndex
CREATE UNIQUE INDEX "filhos_email_key" ON "filhos"("email");

-- AddForeignKey
ALTER TABLE "filhos" ADD CONSTRAINT "filhos_maeId_fkey" FOREIGN KEY ("maeId") REFERENCES "maes"("id") ON DELETE CASCADE ON UPDATE CASCADE;
