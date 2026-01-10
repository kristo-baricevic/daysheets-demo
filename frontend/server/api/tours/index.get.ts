import { db } from "../../db";
import { defineEventHandler } from "h3"

export default defineEventHandler(() => db.tours);
